import random

from datetime import datetime
from sqlalchemy import desc, text
from sqlalchemy.dialects.mysql import insert

from database import get_grid_answers, to_dict
from models import Condition, Grid, Club, Answer


def create_and_insert_grid(db, app, min_clubs_per_cell=5, grid_date=datetime.now()):
    row_conditions, column_conditions = generate_grid(min_clubs_per_cell)

    insert_new_grid(db, app, row_conditions, column_conditions, grid_date)


def generate_grid(min_clubs_per_cell):
    all_conditions = Condition.query.all()

    while True:

        conditions_sample = random.sample(all_conditions, 6)

        row_conditions = conditions_sample[:3]
        col_conditions = conditions_sample[3:]

        if check_grid_is_possible(row_conditions, col_conditions, min_clubs_per_cell):
            return row_conditions, col_conditions


def check_grid_is_possible(row_conditions, column_conditions, min_clubs_per_cell):

    for row_condition in row_conditions:
        for col_condition in column_conditions:
            possible_clubs = Club.query.filter(text(row_condition.expression), text(col_condition.expression)).all()

            if len(possible_clubs) < min_clubs_per_cell:
                return False

    return True


def insert_new_grid(db, app, row_conditions, column_conditions, grid_date):
    new_grid_id = Grid.query.order_by(desc(Grid.id)).first().id + 1

    new_grid = Grid(
        id=new_grid_id,
        starting_date=grid_date,
        row_condition_1=row_conditions[0].id,
        row_condition_2=row_conditions[1].id,
        row_condition_3=row_conditions[2].id,
        column_condition_1=column_conditions[0].id,
        column_condition_2=column_conditions[1].id,
        column_condition_3=column_conditions[2].id,
    )

    new_grid_answers = get_grid_answers(new_grid, app)

    with app.app_context():

        stmt = insert(Grid).values(
            id=new_grid_id,
            starting_date=grid_date,
            row_condition_1=row_conditions[0].id,
            row_condition_2=row_conditions[1].id,
            row_condition_3=row_conditions[2].id,
            column_condition_1=column_conditions[0].id,
            column_condition_2=column_conditions[1].id,
            column_condition_3=column_conditions[2].id,
        )

        stmt = stmt.on_duplicate_key_update(stmt.inserted)
        db.session.execute(stmt)

        stmt = insert(Answer).values([to_dict(answer) for answer in new_grid_answers])
        stmt = stmt.on_duplicate_key_update(grid_id=stmt.inserted.grid_id)  # ignore update
        db.session.execute(stmt)

        db.session.commit()