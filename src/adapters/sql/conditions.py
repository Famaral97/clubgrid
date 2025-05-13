from sqlalchemy.dialects.mysql import insert

from src.adapters.sql import db
from src.helpers import to_dict
from src.models.condition import Condition


def insert_all(all_conditions, app):
    with app.app_context():
        stmt = insert(Condition).values([to_dict(condition) for condition in all_conditions])
        stmt = stmt.on_duplicate_key_update(stmt.inserted)
        db.session.execute(stmt)
        db.session.commit()


def get_for_grid(grid):
    row_conditions = [
        Condition.query.get(grid.row_condition_1),
        Condition.query.get(grid.row_condition_2),
        Condition.query.get(grid.row_condition_3),
    ]

    col_conditions = [
        Condition.query.get(grid.column_condition_1),
        Condition.query.get(grid.column_condition_2),
        Condition.query.get(grid.column_condition_3),
    ]

    return {'rows': row_conditions, 'cols': col_conditions}
