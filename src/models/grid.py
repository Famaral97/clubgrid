from src.adapters.sql import db


class Grid(db.Model):
    __tablename__ = 'grids'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    starting_date = db.Column(db.DateTime)
    type_id = db.Column(db.Integer, db.ForeignKey('grid_types.id'))
    local_id = db.Column(db.Integer)
    row_condition_1 = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    row_condition_2 = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    row_condition_3 = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    column_condition_1 = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    column_condition_2 = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    column_condition_3 = db.Column(db.Integer, db.ForeignKey('conditions.id'))