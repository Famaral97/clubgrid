from dataclasses import dataclass
from dotenv import load_dotenv
import os
from sqlalchemy import desc, text

from flask import Flask, render_template, jsonify, request

from database import create_default_conditions, create_default_clubs, create_default_grids
from models import db, Condition, Club, Grid, Answer

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
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()
    print(db.metadata)

create_default_conditions(db, app)
create_default_clubs(db, app)
create_default_grids(db, app)


@app.route('/', methods=['GET'])
@app.route('/grid/<grid_id>', methods=['GET'])
def index(grid_id=None):
    if grid_id is None:
        grid = Grid.query.order_by(desc(Grid.id)).first()
    else:
        grid = Grid.query.get(grid_id)

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
                           grid_id=grid.id
                           )


@app.route("/grids", methods=['GET'])
def get_grids():
    grids = Grid.query.order_by(desc(Grid.id)).all()

    grids_ids = [grid.id for grid in grids]

    return jsonify(grids_ids)


@app.route('/clubs', methods=['GET'])
def get_clubs():
    @dataclass
    class ClubRepresenter():
        id: int
        name: str
        logo: str

    clubs = Club.query.all()

    clubs_basic_info = [
        ClubRepresenter(id=club.id, name=club.name, logo=club.logo) for club in clubs
    ]

    return jsonify(clubs_basic_info)


@app.route('/answer', methods=['POST'])
def check_answer():
    data = request.get_json()

    club_id = data["club-id"]
    row_condition_id = int(data["row-condition-id"])
    column_condition_id = int(data["column-condition-id"])
    grid_id = int(data["grid-id"])

    condition_1_expression = Condition.query.get(row_condition_id).expression
    condition_2_expression = Condition.query.get(column_condition_id).expression

    club = Club.query.get(club_id)

    solution_clubs = Club.query.filter(Club.id == club_id, text(condition_1_expression),
                                       text(condition_2_expression)).all()

    result = len(solution_clubs) == 1

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

    return jsonify({"correct": result, "clubName": club.name, "logo": club.logo})


@app.route('/grid/<grid_id>/end', methods=['GET'])
def get_grid_solution(grid_id):
    grid = Grid.query.get(grid_id)

    solutions = [
        [
            get_solution(grid_id, grid.row_condition_1, grid.column_condition_1),
            get_solution(grid_id, grid.row_condition_1, grid.column_condition_2),
            get_solution(grid_id, grid.row_condition_1, grid.column_condition_3)
        ],
        [
            get_solution(grid_id, grid.row_condition_2, grid.column_condition_1),
            get_solution(grid_id, grid.row_condition_2, grid.column_condition_2),
            get_solution(grid_id, grid.row_condition_2, grid.column_condition_3)
        ],
        [
            get_solution(grid_id, grid.row_condition_3, grid.column_condition_1),
            get_solution(grid_id, grid.row_condition_3, grid.column_condition_2),
            get_solution(grid_id, grid.row_condition_3, grid.column_condition_3)
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


def get_solution(grid_id, row_condition_id, col_condition_id):
    @dataclass
    class ClubRepresenter():
        id: int
        name: str
        logo: str
        answer_count: int

    row_condition = Condition.query.get(row_condition_id)
    col_condition = Condition.query.get(col_condition_id)

    solution_clubs = Club.query.filter(text(row_condition.expression), text(col_condition.expression)).all()

    clubs_representers = []

    total_guesses = 0

    for club in solution_clubs:
        answer = Answer.query.filter(
            Answer.grid_id == grid_id,
            Answer.club_id == club.id,
            Answer.row_condition_id == row_condition_id,
            Answer.column_condition_id == col_condition_id,
        ).one_or_none()

        answer_count = answer.count if answer is not None else 0

        clubs_representers.append(
            ClubRepresenter(id=club.id, name=club.name, logo=club.logo, answer_count=answer_count)
        )

        total_guesses += answer_count

    return {"clubs": clubs_representers, "total_guesses": total_guesses}
