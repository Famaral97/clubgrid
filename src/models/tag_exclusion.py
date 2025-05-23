from src.adapters.sql import db


class TagExclusion(db.Model):
    __tablename__ = 'tag_exclusions'
    grid_type_id = db.Column(db.Integer, db.ForeignKey('grid_types.id'), primary_key=True)
    tag = db.Column(db.String(255), primary_key=True)
