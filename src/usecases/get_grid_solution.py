from dataclasses import dataclass

from sqlalchemy import text

import src.adapters.sql.conditions as conditions_adapter

from src.models.answer import Answer
from src.models.club import Club
from src.models.condition import Condition
from src.models.grid import Grid
from src.models.grid_type import GridType


def get_grid_solution(grid_id):
    grid = Grid.query.get(grid_id)
    grid_type = GridType.query.get(grid.type_id)

    solutions = [
        [
            get_solution(grid_id, grid.row_condition_1, grid.column_condition_1, grid_type),
            get_solution(grid_id, grid.row_condition_1, grid.column_condition_2, grid_type),
            get_solution(grid_id, grid.row_condition_1, grid.column_condition_3, grid_type)
        ],
        [
            get_solution(grid_id, grid.row_condition_2, grid.column_condition_1, grid_type),
            get_solution(grid_id, grid.row_condition_2, grid.column_condition_2, grid_type),
            get_solution(grid_id, grid.row_condition_2, grid.column_condition_3, grid_type)
        ],
        [
            get_solution(grid_id, grid.row_condition_3, grid.column_condition_1, grid_type),
            get_solution(grid_id, grid.row_condition_3, grid.column_condition_2, grid_type),
            get_solution(grid_id, grid.row_condition_3, grid.column_condition_3, grid_type)
        ]
    ]

    conditions = conditions_adapter.get_for_grid(grid)

    return solutions, conditions


# TODO: move part of this logic to the database.py since it has a very similar method
def get_solution(grid_id, row_condition_id, col_condition_id, grid_type):
    @dataclass
    class ClubRepresenter:
        id: str
        total_club_answered: int

    query = Club.query.filter(
        text(Condition.query.get(row_condition_id).expression),
        text(Condition.query.get(col_condition_id).expression)
    )

    if grid_type is not None:
        query = query.filter(text(grid_type.expression))

    solution_clubs = query.all()

    clubs_representers = []

    total_correct_answers = 0

    for club in solution_clubs:
        answer = Answer.query.filter(
            Answer.grid_id == grid_id,
            Answer.club_id == club.id,
            Answer.row_condition_id == row_condition_id,
            Answer.column_condition_id == col_condition_id,
        ).one_or_none()

        total_club_answered = answer.count if answer is not None else 0

        clubs_representers.append(
            ClubRepresenter(id=club.id, total_club_answered=total_club_answered)
        )

        total_correct_answers += total_club_answered

    sorted_club_representers = sorted(clubs_representers, key=lambda c: c.total_club_answered, reverse=True)

    return {"solution_clubs": sorted_club_representers, "total_correct_answers": total_correct_answers}
