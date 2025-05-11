import csv
from datetime import datetime, timedelta

from sqlalchemy import text, inspect, desc
from sqlalchemy.dialects.mysql import insert

from src.models.answer import Answer
from src.models.club import Club
from src.models.condition import Condition
from src.models.grid import Grid
from src.models.grid_type import GridType


def get_grid_answers(grid, app):
    with app.app_context():
        grid_type_id = grid.type_id if grid.type_id else 1
        grid_type = GridType.query.get(grid_type_id)

    grid_answers = []
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_1, grid.row_condition_1, grid_type, app))
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_1, grid.row_condition_2, grid_type, app))
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_1, grid.row_condition_3, grid_type, app))
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_2, grid.row_condition_1, grid_type, app))
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_2, grid.row_condition_2, grid_type, app))
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_2, grid.row_condition_3, grid_type, app))
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_3, grid.row_condition_1, grid_type, app))
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_3, grid.row_condition_2, grid_type, app))
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_3, grid.row_condition_3, grid_type, app))
    return grid_answers


def get_cell_answers(grid, column_condition_id, row_condition_id, grid_type, app):
    with app.app_context():
        query = Club.query.filter(
            text(Condition.query.get(row_condition_id).expression),
            text(Condition.query.get(column_condition_id).expression)
        )

        if grid_type is not None:
            query = query.filter(text(grid_type.expression))

        solution_clubs = query.all()

    return [Answer(
        grid_id=grid.id,
        column_condition_id=column_condition_id,
        row_condition_id=row_condition_id,
        club_id=club.id,
        is_solution=True,
        count=0,
    ) for club in solution_clubs]


def get_grid_solution(row_conditions, column_conditions, grid_type, app):
    return [
        [
            get_cell_solution(row_conditions[0], column_conditions[0], grid_type, app),
            get_cell_solution(row_conditions[0], column_conditions[1], grid_type, app),
            get_cell_solution(row_conditions[0], column_conditions[2], grid_type, app)
        ],
        [
            get_cell_solution(row_conditions[1], column_conditions[0], grid_type, app),
            get_cell_solution(row_conditions[1], column_conditions[1], grid_type, app),
            get_cell_solution(row_conditions[1], column_conditions[2], grid_type, app)
        ],
        [
            get_cell_solution(row_conditions[2], column_conditions[0], grid_type, app),
            get_cell_solution(row_conditions[2], column_conditions[1], grid_type, app),
            get_cell_solution(row_conditions[2], column_conditions[2], grid_type, app)
        ]
    ]


def get_cell_solution(row_condition, col_condition, grid_type, app):
    with app.app_context():
        query = Club.query.filter(text(row_condition.expression), text(col_condition.expression))

        if grid_type is not None:
            query = query.filter(text(grid_type.expression))

        solution_clubs = query.all()

    return solution_clubs


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
