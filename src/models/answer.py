from src.adapters.sql import db


class Answer(db.Model):
    __tablename__ = 'answers'

    grid_id = db.Column(db.Integer, db.ForeignKey('grids.id'), primary_key=True)
    row_condition_id = db.Column(db.Integer, db.ForeignKey('conditions.id'), primary_key=True)
    column_condition_id = db.Column(db.Integer, db.ForeignKey('conditions.id'), primary_key=True)
    club_id = db.Column(db.String(255), db.ForeignKey('clubs.id'), primary_key=True)
    count = db.Column(db.Integer)
