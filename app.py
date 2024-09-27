from dataclasses import dataclass
from dotenv import load_dotenv
import os
from sqlalchemy import desc

from flask import Flask, render_template, jsonify, request

from database import create_default_conditions, create_default_clubs, create_default_grids
from models import db, Condition, Club, Grid

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
    condition_1_id = data["condition-id-1"]
    condition_2_id = data["condition-id-2"]

    condition_1_expression = Condition.query.get(int(condition_1_id)).expression
    condition_2_expression = Condition.query.get(int(condition_2_id)).expression

    club = Club.query.get(club_id)

    result = eval(condition_1_expression) and eval(condition_2_expression)

    return jsonify({"correct": result, "clubName": club.name, "logo": club.logo})



