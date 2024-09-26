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
    country = db.Column(db.String(255))
    logo = db.Column(db.String(255))
    league = db.Column(db.String(255))

    has_animal = db.Column(db.Boolean)
    has_winged_animal = db.Column(db.Boolean)
    has_person = db.Column(db.Boolean)
    has_football = db.Column(db.Boolean)
    stars_number = db.Column(db.Integer)
    colors_number = db.Column(db.String(50))
    has_numbers = db.Column(db.Boolean)
    has_color_red = db.Column(db.Boolean)
    has_color_blue = db.Column(db.Boolean)


class Grid(db.Model):
    __tablename__ = 'grids'
    id = db.Column(db.Integer, primary_key=True)
    row_condition_1 = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    row_condition_2 = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    row_condition_3 = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    column_condition_1 = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    column_condition_2 = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    column_condition_3 = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    starting_date = db.Column(db.Date)
