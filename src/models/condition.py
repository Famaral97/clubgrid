from src.adapters.sql import db


class Condition(db.Model):
    __tablename__ = 'conditions'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    expression = db.Column(db.Text())
    tag = db.Column(db.String(255))
    deprecated = db.Column(db.Boolean)
