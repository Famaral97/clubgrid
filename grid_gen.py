import random

from datetime import datetime
from sqlalchemy import desc, text
from sqlalchemy.dialects.mysql import insert

from database import get_grid_answers, to_dict
from models import Condition, Grid, Club, Answer


def create_and_insert_grid(db, app, min_clubs_per_cell=5, grid_date=datetime.now(), max_common_conditions=2, previous_grids_number=3):
    row_conditions, column_conditions = generate_grid(min_clubs_per_cell, max_common_conditions, previous_grids_number)

    insert_new_grid(db, app, row_conditions, column_conditions, grid_date)

    ids = []
    for row_cond in row_conditions:
        ids.append(row_cond.id)
    for column_cond in column_conditions:
        ids.append(column_cond.id)
    return ids


def generate_grid(min_clubs_per_cell, max_common_conditions, previous_grids_number):
    all_conditions = Condition.query.all()
    all_grids = Grid.query.order_by(desc(Grid.id)).all()

    conditions_weights = compute_weights(all_conditions, all_grids)

    while True:

        conditions_sample = get_weighted_sample_of_conditions(all_conditions, conditions_weights)

        row_conditions = conditions_sample[:3]
        col_conditions = conditions_sample[3:]

        if check_grid_is_possible(row_conditions, col_conditions, min_clubs_per_cell) and \
                check_grid_does_not_have_common_conditions_to_last_n_grids(conditions_sample, all_grids, previous_grids_number) and \
                check_grid_is_not_too_similar(conditions_sample, all_grids, max_common_conditions) and \
                check_grid_has_different_conditions_tags(conditions_sample):
            return row_conditions, col_conditions


def get_weighted_sample_of_conditions(conditions, weights):
    selected_conditions = []

    while len(selected_conditions) < 6:
        random_condition = random.choices(conditions, weights=weights)[0]
        if random_condition not in selected_conditions:
            selected_conditions.append(random_condition)
    return selected_conditions


def compute_weights(conditions, grids):
    weights_by_condition_id = {}
    for grid in grids:
        weights_by_condition_id[grid.row_condition_1] = weights_by_condition_id.get(grid.row_condition_1, 0) + 1
        weights_by_condition_id[grid.row_condition_2] = weights_by_condition_id.get(grid.row_condition_2, 0) + 1
        weights_by_condition_id[grid.row_condition_3] = weights_by_condition_id.get(grid.row_condition_3, 0) + 1

        weights_by_condition_id[grid.column_condition_1] = weights_by_condition_id.get(grid.column_condition_1, 0) + 1
        weights_by_condition_id[grid.column_condition_2] = weights_by_condition_id.get(grid.column_condition_2, 0) + 1
        weights_by_condition_id[grid.column_condition_3] = weights_by_condition_id.get(grid.column_condition_3, 0) + 1

    weights_list = []
    for condition in conditions:
        weight = 1 / (1 + weights_by_condition_id.get(condition.id, 0))
        weights_list.append(weight)

    return weights_list


def check_grid_has_different_conditions_tags(conditions):
    tags = [condition.tags for condition in conditions]
    return len(set(tags)) == 6


def check_grid_does_not_have_common_conditions_to_last_n_grids(conditions, grids, n_grids):
    conditions_ids = [condition.id for condition in conditions]

    for grid in grids[:n_grids]:
        grid_conditions = [
            grid.row_condition_1,
            grid.row_condition_2,
            grid.row_condition_3,
            grid.column_condition_1,
            grid.column_condition_2,
            grid.column_condition_3
        ]
        common_conditions = list(set(conditions_ids).intersection(grid_conditions))
        if len(common_conditions) > 0:
            return False
    return True


def check_grid_is_not_too_similar(conditions, grids, max_conditions_number):
    conditions_ids = [condition.id for condition in conditions]

    for grid in grids:
        grid_conditions = [
            grid.row_condition_1,
            grid.row_condition_2,
            grid.row_condition_3,
            grid.column_condition_1,
            grid.column_condition_2,
            grid.column_condition_3
        ]
        common_conditions = list(set(conditions_ids).intersection(grid_conditions))
        if len(common_conditions) > max_conditions_number:
            return False
    return True


def check_grid_is_possible(row_conditions, column_conditions, min_clubs_per_cell):
    for row_condition in row_conditions:
        for col_condition in column_conditions:
            print(row_condition.expression)
            print(col_condition.expression)
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
