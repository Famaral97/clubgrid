from src.models.answer import Answer
from sqlalchemy import func


def get_total_answers_count(grid_id, row_condition_id, column_condition_id):
    return int(Answer.query.with_entities(func.sum(Answer.count)).filter(
        Answer.grid_id == grid_id,
        Answer.row_condition_id == row_condition_id,
        Answer.column_condition_id == column_condition_id
    ).scalar() or 0)
