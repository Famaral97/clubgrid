from datetime import datetime, timedelta

from sqlalchemy import inspect, desc
from sqlalchemy.dialects.mysql import insert

from src.models.grid import Grid


def insert_grid(db, app, row_conditions, column_conditions, grid_type):
    newest_local_grid = Grid.query.filter(Grid.type_id == grid_type.id).order_by(desc(Grid.local_id)).first()
    grid_local_id = (newest_local_grid.local_id if newest_local_grid else 0) + 1

    latest_grid = Grid.query.order_by(desc(Grid.id)).filter(Grid.type_id == grid_type.id).first()
    new_grid_date = latest_grid.starting_date + timedelta(days=1) if latest_grid \
        else datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)

    new_grid = Grid(
        local_id=grid_local_id,
        type_id=grid_type.id,
        starting_date=new_grid_date,
        row_condition_1=row_conditions[0].id,
        row_condition_2=row_conditions[1].id,
        row_condition_3=row_conditions[2].id,
        column_condition_1=column_conditions[0].id,
        column_condition_2=column_conditions[1].id,
        column_condition_3=column_conditions[2].id,
    )

    with app.app_context():
        stmt = insert(Grid).values(to_dict(new_grid))
        result = db.session.execute(stmt)
        db.session.commit()

        new_grid.id = result.lastrowid

        db.session.commit()


def to_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


def to_int(s):
    s = s.replace('€', '')

    if '+-0' in s:
        return 0

    if s[-1] == 'm':
        multiplier = 1_000_000
    elif s[-1] == 'k':
        multiplier = 1_000
    else:
        raise ValueError("Invalid suffix. Only 'm' and 'k' are supported.")

    numeric_part = float(s[:-1])

    return int(numeric_part * multiplier)
