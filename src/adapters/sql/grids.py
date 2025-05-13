
from src.adapters.sql import db

from sqlalchemy import text
from sqlalchemy.dialects.mysql import insert

from src.helpers import to_dict
from src.models.club import Club
from src.models.grid import Grid


def insert_all(grids, app):
    with app.app_context():
        stmt = insert(Grid).values([to_dict(grid) for grid in grids])
        stmt = stmt.on_duplicate_key_update(stmt.inserted)

        db.session.execute(stmt)

        db.session.commit()


def insert_without_id(grid, app):
    with app.app_context():
        stmt = insert(Grid).values(to_dict(grid))
        result = db.session.execute(stmt)
        db.session.commit()

        grid.id = result.lastrowid

        db.session.commit()


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
