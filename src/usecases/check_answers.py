from src.adapters.sql import db
from src.models.answer import Answer
from src.models.club import Club
from src.models.condition import Condition
from src.models.grid import Grid
from src.models.grid_type import GridType
import src.adapters.sql.grids as grids_adapter
from sqlalchemy.dialects.mysql import insert
import src.adapters.sql.answers as answers_adapter


def check_answer(club_id, row_condition_id, column_condition_id, grid_id, app):
    club = Club.query.get(club_id)

    answer = Answer.query.get((grid_id, row_condition_id, column_condition_id, club.id))

    row_condition = Condition.query.get(row_condition_id)
    column_condition = Condition.query.get(column_condition_id)
    grid_type = GridType.query.get(Grid.query.get(grid_id).type_id)

    is_correct = club in grids_adapter.get_cell_solution(row_condition, column_condition, grid_type, app)

    total_answers = -1
    total_club_answered = -1
    if is_correct:
        total_club_answered = 0 if answer is None else answer.count
        total_answers = answers_adapter.get_total_answers_count(grid_id, row_condition.id, column_condition.id)

    stmt = insert(Answer).values(
        grid_id=grid_id,
        club_id=club.id,
        row_condition_id=row_condition_id,
        column_condition_id=column_condition_id,
        count=1,
    ).on_duplicate_key_update(count=Answer.count + 1)

    with app.app_context():
        db.session.execute(stmt)
        db.session.commit()

    return is_correct, club, total_club_answered, total_answers
