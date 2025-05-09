from dataclasses import dataclass
from datetime import datetime

from dotenv import load_dotenv
import os

from sqlalchemy import desc, text, func

from flask import Flask, render_template, jsonify, redirect, request

from database import create_default_clubs, create_default_grids, \
    create_default_grid_types, load_conditions
from grid_gen import create_and_insert_grid
from models import db, Condition, Club, Grid, Answer, GridType

from sqlalchemy.dialects.mysql import insert

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

load_conditions(db, app)
create_default_grid_types(db, app)
create_default_clubs(db, app)

# create_default_grids(db, app)


@app.route('/health-check')
def health_check():
    return jsonify({"status": "Up"})


# to test grid generation
@app.route(f'/{os.getenv("GRID_GENERATION_ENDPOINT")}', methods=['POST'])
def generate_grid():
    grid_type_id = request.args.get('grid_type_id')

    if grid_type_id is None:
        return jsonify({"error": "grid_type_id is required"}), 400

    return f"{create_and_insert_grid(db, app, grid_type_id)}"


@app.route('/', methods=['GET'])
def redirect_home():
    latest_grid_id = Grid.query.order_by(desc(Grid.id)).filter(Grid.starting_date <= datetime.now()).first().id
    return redirect(f"/grid/{latest_grid_id}", code=302)


@app.route('/grid/<grid_id>', methods=['GET'])
def index(grid_id):
    grid = Grid.query.get(grid_id)
    grid_type = GridType.query.get(grid.type_id)

    if grid.starting_date > datetime.now():
        return redirect(f"/", code=302)

    row_conditions = [
        Condition.query.get(grid.row_condition_1),
        Condition.query.get(grid.row_condition_2),
        Condition.query.get(grid.row_condition_3),
    ]

    col_conditions = [
        Condition.query.get(grid.column_condition_1),
        Condition.query.get(grid.column_condition_2),
        Condition.query.get(grid.column_condition_3),
    ]

    return render_template('index.html',
                           row_conditions=row_conditions,
                           col_conditions=col_conditions,
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
            shortName=club.short_name,
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

    is_correct = answer.is_solution if answer is not None else False

    total_answers = -1
    total_club_answered = -1
    if is_correct:
        total_club_answered = answer.count
        total_answers = int(Answer.query.with_entities(func.sum(Answer.count)).filter(
            Answer.grid_id == grid_id,
            Answer.row_condition_id == row_condition_id,
            Answer.column_condition_id == column_condition_id
        ).scalar())

    stmt = insert(Answer).values(
        grid_id=grid_id,
        club_id=club.id,
        row_condition_id=row_condition_id,
        column_condition_id=column_condition_id,
        is_solution=is_correct,
        count=1,
    )

    stmt = stmt.on_duplicate_key_update(count=Answer.count + 1)

    with app.app_context():
        db.session.execute(stmt)
        db.session.commit()

    return jsonify({
        "correct": is_correct,
        "clubShortName": club.short_name,
        "logo": club.logo,
        "total_club_answered": total_club_answered,
        "total_answers": total_answers
    })


@app.route('/grid/<grid_id>/end', methods=['GET'])
def get_grid_solution(grid_id):
    grid = Grid.query.get(grid_id)
    grid_type = GridType.query.get(grid.type_id)

    solutions = [
        [
            get_solution(grid_id, grid.row_condition_1, grid.column_condition_1, grid_type),
            get_solution(grid_id, grid.row_condition_1, grid.column_condition_2, grid_type),
            get_solution(grid_id, grid.row_condition_1, grid.column_condition_3, grid_type)
        ],
        [
            get_solution(grid_id, grid.row_condition_2, grid.column_condition_1, grid_type),
            get_solution(grid_id, grid.row_condition_2, grid.column_condition_2, grid_type),
            get_solution(grid_id, grid.row_condition_2, grid.column_condition_3, grid_type)
        ],
        [
            get_solution(grid_id, grid.row_condition_3, grid.column_condition_1, grid_type),
            get_solution(grid_id, grid.row_condition_3, grid.column_condition_2, grid_type),
            get_solution(grid_id, grid.row_condition_3, grid.column_condition_3, grid_type)
        ]
    ]

    row_conditions = [
        Condition.query.get(grid.row_condition_1).description,
        Condition.query.get(grid.row_condition_2).description,
        Condition.query.get(grid.row_condition_3).description,
    ]

    col_conditions = [
        Condition.query.get(grid.column_condition_1).description,
        Condition.query.get(grid.column_condition_2).description,
        Condition.query.get(grid.column_condition_3).description,
    ]

    return jsonify(
        {
            "solutions": solutions,
            "row_conditions_descriptions": row_conditions,
            "col_conditions_descriptions": col_conditions
        }
    )


# TODO: move part of this logic to the database.py since it has a very similar method
def get_solution(grid_id, row_condition_id, col_condition_id, grid_type):
    @dataclass
    class ClubRepresenter():
        id: str
        total_club_answered: int

    query = Club.query.filter(
        text(Condition.query.get(row_condition_id).expression),
        text(Condition.query.get(col_condition_id).expression)
    )

    if grid_type is not None:
        query = query.filter(text(grid_type.expression))

    solution_clubs = query.all()

    clubs_representers = []

    total_correct_answers = 0

    for club in solution_clubs:
        answer = Answer.query.filter(
            Answer.grid_id == grid_id,
            Answer.club_id == club.id,
            Answer.row_condition_id == row_condition_id,
            Answer.column_condition_id == col_condition_id,
        ).one_or_none()

        total_club_answered = answer.count if answer is not None else 0

        clubs_representers.append(
            ClubRepresenter(id=club.id, total_club_answered=total_club_answered)
        )

        total_correct_answers += total_club_answered

    sorted_club_representers = sorted(clubs_representers, key=lambda c: c.total_club_answered, reverse=True)

    return {"solution_clubs": sorted_club_representers, "total_correct_answers": total_correct_answers}
