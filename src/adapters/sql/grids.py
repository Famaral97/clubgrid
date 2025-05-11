from sqlalchemy.dialects.mysql import insert

from src.adapters.database import to_dict
from src.adapters.sql import db
from src.models.grid import Grid


def insert_grids(grids, app):
    with app.app_context():
        stmt = insert(Grid).values([to_dict(grid) for grid in grids])
        stmt = stmt.on_duplicate_key_update(stmt.inserted)

        db.session.execute(stmt)

        db.session.commit()
