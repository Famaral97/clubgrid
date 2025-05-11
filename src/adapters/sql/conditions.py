from sqlalchemy.dialects.mysql import insert

from src.adapters.database import to_dict
from src.adapters.sql import db
from src.models.condition import Condition


def insert_conditions(all_conditions, app):
    with app.app_context():
        stmt = insert(Condition).values([to_dict(condition) for condition in all_conditions])
        stmt = stmt.on_duplicate_key_update(stmt.inserted)
        db.session.execute(stmt)
        db.session.commit()
