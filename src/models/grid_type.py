from src.adapters.sql import db


class GridType(db.Model):
    __tablename__ = 'grid_types'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    expression = db.Column(db.String(255))
    exclude_country_conditions = db.Column(db.Boolean)
