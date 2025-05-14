from dataclasses import dataclass
from datetime import datetime

from dotenv import load_dotenv
import os

from sqlalchemy import desc, text, func

from flask import Flask, render_template, jsonify, redirect, request

import src.adapters.csv as csv_adapter
import src.adapters.sql.clubs as clubs_adapter
import src.adapters.sql.conditions as conditions_adapter
import src.adapters.sql.grid_types as grid_types_adapter
import src.adapters.sql.grids as grids_adapter
from src.models.UnauthorizedGridException import UnauthorizedGridException
from src.usecases.generate_grid import generate_grid
from src.adapters.sql import db
from src.models.answer import Answer
from src.models.club import Club
from src.models.condition import Condition
from src.models.grid import Grid
from src.models.grid_type import GridType
from sqlalchemy.dialects.mysql import insert

import src.adapters.yaml as yaml_adapter
from src.adapters import local_memory
from src.usecases.get_grid_solution import get_grid_solution
from src.usecases.render_index import render_index

app = Flask(__name__)

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    hostname=os.getenv("DB_HOSTNAME"),
    databasename=os.getenv("DB_NAME")
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 280,
    'pool_pre_ping': True
}
db.init_app(app)

conditions = yaml_adapter.load_conditions()
conditions_adapter.insert_all(conditions, app)

grid_types = yaml_adapter.load_grid_types()
grid_types_adapter.insert_all(grid_types, app)

clubs = csv_adapter.load_clubs()
clubs_adapter.insert_all(clubs, app)

grids_adapter.insert_all(local_memory.grids, app)


@app.route('/health-check')
def health_check():
    return jsonify({"status": "Up"})


# to test grid generation
@app.route(f'/{os.getenv("GRID_GENERATION_ENDPOINT")}', methods=['POST'])
def generate_grid_handler():
    grid_type_id = request.args.get('grid_type_id')

    if grid_type_id is None:
        return jsonify({"error": "grid_type_id is required"}), 400

    return f"{generate_grid(app, grid_type_id)}"


@app.route('/', methods=['GET'])
def redirect_home():
    latest_grid_id = Grid.query.order_by(desc(Grid.id)).filter(Grid.starting_date <= datetime.now()).first().id
    return redirect(f"/grid/{latest_grid_id}", code=302)


@app.route('/grid/<grid_id>', methods=['GET'])
def index(grid_id):
    try:
        grid, grid_type, grid_conditions = render_index(grid_id)
    except UnauthorizedGridException as e:
        return redirect(f"/", code=302)

    return render_template(
        template_name_or_list='index.html',
        row_conditions=grid_conditions['rows'],
        col_conditions=grid_conditions['cols'],
        grid_id=grid.id,
        grid_type_description=grid_type.description
    )


@app.route("/grids", methods=['GET'])
def get_grids():
    result = (db.session.query(Grid, GridType)
              .join(GridType, Grid.type_id == GridType.id)
              .filter(Grid.starting_date <= datetime.now())
              .order_by(desc(Grid.id))
              .all())

    @dataclass
    class GridRepresenter():
        id: int
        type_description: str
        starting_date: str

    grids = [GridRepresenter(
        id=grid.id,
        type_description=grid_type.description,
        starting_date=grid.starting_date.strftime('%a, %d %b')
    ) for grid, grid_type in result]

    return jsonify(grids)


@app.route('/clubs', methods=['GET'])
def get_clubs():
    @dataclass
    class ClubRepresenter():
        id: int
        name: str
        shortName: str
        logo: str

    clubs = Club.query.all()

    clubs_basic_info = {
        club.id: ClubRepresenter(
            id=club.id,
            name=club.name,
            shortName=club.name,
            logo=club.logo
        ) for club in clubs
    }

    return jsonify(clubs_basic_info)


@app.route('/answer', methods=['POST'])
def check_answer():
    data = request.get_json()

    club_id = data["club-id"]
    row_condition_id = int(data["row-condition-id"])
    column_condition_id = int(data["column-condition-id"])
    grid_id = int(data["grid-id"])

    club = Club.query.get(club_id)

    answer = Answer.query.get((grid_id, row_condition_id, column_condition_id, club.id))

    row_condition = Condition.query.get(row_condition_id)
    column_condition = Condition.query.get(column_condition_id)
    grid_type = GridType.query.get(Grid.query.get(grid_id).type_id)
    is_correct = club in grids_adapter.get_cell_solution(row_condition, column_condition, grid_type, app)

    total_answers = -1
    total_club_answered = -1
    if is_correct:
        total_club_answered = 0 if answer is None else answer.count
        total_answers = int(Answer.query.with_entities(func.sum(Answer.count)).filter(
            Answer.grid_id == grid_id,
            Answer.row_condition_id == row_condition_id,
            Answer.column_condition_id == column_condition_id
        ).scalar() or 0)

    stmt = insert(Answer).values(
        grid_id=grid_id,
        club_id=club.id,
        row_condition_id=row_condition_id,
        column_condition_id=column_condition_id,
        count=1,
    )

    stmt = stmt.on_duplicate_key_update(count=Answer.count + 1)

    with app.app_context():
        db.session.execute(stmt)
        db.session.commit()

    return jsonify({
        "correct": is_correct,
        "clubShortName": club.name,
        "logo": club.logo,
        "total_club_answered": total_club_answered,
        "total_answers": total_answers
    })


@app.route('/grid/<grid_id>/end', methods=['GET'])
def get_grid_solution_handler(grid_id):
    solutions_with_answers, grid_conditions = get_grid_solution(grid_id, app)

    @dataclass
    class ClubSolutionRepresenter:
        id: str
        total_club_answered: int

    @dataclass
    class CellSolutionRepresenter:
        solution_clubs: list[ClubSolutionRepresenter]
        total_correct_answers: int

    @dataclass
    class GridSolutionRepresenter:
        col_conditions_descriptions: list[str]
        row_conditions_descriptions: list[str]
        solutions: list[list[CellSolutionRepresenter]]

    solutions_representer = [
        [
            CellSolutionRepresenter(
                solution_clubs=[
                    ClubSolutionRepresenter(
                        id=club.id,
                        total_club_answered=answer.count if answer is not None else 0
                    ) for club, answer in cell
                ],
                total_correct_answers=sum(answer.count if answer is not None else 0 for _, answer in cell)
            ) for cell in row
        ] for row in solutions_with_answers
    ]

    return jsonify(
        GridSolutionRepresenter(
            col_conditions_descriptions=[col_condition.description for col_condition in grid_conditions['cols']],
            row_conditions_descriptions=[row_condition.description for row_condition in grid_conditions['rows']],
            solutions=solutions_representer
        )
    )
