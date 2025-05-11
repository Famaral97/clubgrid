from sqlalchemy.dialects.mysql import insert

from src.adapters.database import to_dict
from src.adapters.sql import db
from src.models.club import Club


def insert_clubs(all_clubs, app):
    with app.app_context():
        stmt = insert(Club).values([to_dict(club) for club in all_clubs])
        stmt = stmt.on_duplicate_key_update(stmt.inserted)
        db.session.execute(stmt)
        db.session.commit()
