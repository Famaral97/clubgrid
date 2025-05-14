from src.adapters.sql import db

from sqlalchemy import text, and_
from sqlalchemy.dialects.mysql import insert

from src.helpers import to_dict
from src.models.answer import Answer
from src.models.club import Club
from src.models.condition import Condition
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


def get_solutions_with_answers(grid, grid_type, app):
    row_conditions = [
        Condition.query.get(grid.row_condition_1),
        Condition.query.get(grid.row_condition_2),
        Condition.query.get(grid.row_condition_3),
    ]
    column_conditions = [
        Condition.query.get(grid.column_condition_1),
        Condition.query.get(grid.column_condition_2),
        Condition.query.get(grid.column_condition_3),
    ]

    return [
        [
            get_cell_solution(row_cond, col_cond, grid_type, app, grid.id) for col_cond in column_conditions
        ] for row_cond in row_conditions
    ]


def get_solutions(row_conditions, col_conditions, grid_type, app):
    return [
        [
            get_cell_solution(row_conditions[row_idx], col_conditions[col_idx], grid_type, app) for col_idx in range(3)
        ] for row_idx in range(3)
    ]


def get_cell_solution(row_condition, col_condition, grid_type, app, include_answers_of_grid_id=None):
    with app.app_context():
        query = Club.query.filter(text(row_condition.expression), text(col_condition.expression))

        if grid_type is not None:
            query = query.filter(text(grid_type.expression))

        if include_answers_of_grid_id is not None:
            query = query.join(Answer, and_(
                Answer.grid_id == include_answers_of_grid_id,
                Answer.club_id == Club.id,
                Answer.row_condition_id == row_condition.id,
                Answer.column_condition_id == col_condition.id
            ), isouter=True).add_entity(Answer)

        solutions_with_answers = query.all()

    return solutions_with_answers
