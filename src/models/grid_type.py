from src.adapters.sql import db

from sqlalchemy import UnicodeText


class GridType(db.Model):
    __tablename__ = 'grid_types'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(UnicodeText)
    expression = db.Column(db.String(255))
