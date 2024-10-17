from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Condition(db.Model):
    __tablename__ = 'conditions'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255)) 
    expression = db.Column(db.String(255))


class Club(db.Model):
    __tablename__ = 'clubs'
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    short_name = db.Column(db.String(255))
    country = db.Column(db.String(255))
    logo = db.Column(db.String(255))
    league = db.Column(db.String(255))

    year_founded = db.Column(db.Integer)
    name_has_number = db.Column(db.Boolean)
    has_animal = db.Column(db.Boolean)
    has_winged_animal = db.Column(db.Boolean)
    has_person = db.Column(db.Boolean)
    has_football = db.Column(db.Boolean)
    stars_number = db.Column(db.Integer)
    colors_number = db.Column(db.String(50))
    has_numbers = db.Column(db.Boolean)
    has_color_red = db.Column(db.Boolean)
    has_color_blue = db.Column(db.Boolean)
    has_color_green = db.Column(db.Boolean)
    has_color_black = db.Column(db.Boolean)
    league_titles = db.Column(db.Integer)
    has_crown = db.Column(db.Boolean)
    champions_league_titles = db.Column(db.Integer)
    champions_league_runner_up = db.Column(db.Integer)
    europa_league_titles = db.Column(db.Integer)
    europa_league_runner_up = db.Column(db.Integer)
    in_capital = db.Column(db.Boolean)
    cup_titles = db.Column(db.Integer)
    cup_runner_up = db.Column(db.Integer)
    is_circular = db.Column(db.Boolean)
    stadium_capacity = db.Column(db.Integer)
    squad_size = db.Column(db.Integer)
    average_age = db.Column(db.Float)
    foreigners_number = db.Column(db.Integer)
    foreigners_percentage = db.Column(db.Float)
    national_team_players = db.Column(db.Integer)
    net_transfer_record = db.Column(db.Integer)


class Grid(db.Model):
    __tablename__ = 'grids'
    id = db.Column(db.Integer, primary_key=True)
    row_condition_1 = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    row_condition_2 = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    row_condition_3 = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    column_condition_1 = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    column_condition_2 = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    column_condition_3 = db.Column(db.Integer, db.ForeignKey('conditions.id'))


class Answer(db.Model):
    __tablename__ = 'answers'

    grid_id = db.Column(db.Integer, db.ForeignKey('grids.id'), primary_key=True)
    row_condition_id = db.Column(db.Integer, db.ForeignKey('conditions.id'), primary_key=True)
    column_condition_id = db.Column(db.Integer, db.ForeignKey('conditions.id'), primary_key=True)
    club_id = db.Column(db.String(255), db.ForeignKey('clubs.id'), primary_key=True)
    is_solution = db.Column(db.Boolean)
    count = db.Column(db.Integer)
