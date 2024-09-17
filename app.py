from dataclasses import dataclass

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from database import create_default_conditions, create_default_clubs
from models import db, Condition, Club

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://flaskuser:flaskpassword@mysql/flaskdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()
    print(db.metadata)

create_default_conditions(db, app)
create_default_clubs(db, app)


@app.route('/grid', methods=['GET', 'POST'])
def index():

    conditions = Condition.query.limit(6).all()

    return render_template('index.html', conditions=conditions)


@app.route('/clubs', methods=['GET', 'POST'])
def get_clubs():

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

    return jsonify({"correct": result, "clubName": club.name, "logo": club.logo })


@dataclass
class ClubRepresenter():
    id: int
    name: str
    logo: str
