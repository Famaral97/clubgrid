from sqlalchemy.dialects.mysql import insert

from src.adapters.sql import db
from src.helpers import to_dict
from src.models.grid_type import GridType


def insert_grid_types(all_grid_types, app):
    with app.app_context():
        stmt = insert(GridType).values([to_dict(grid_type) for grid_type in all_grid_types])
        stmt = stmt.on_duplicate_key_update(stmt.inserted)
        db.session.execute(stmt)
        db.session.commit()
