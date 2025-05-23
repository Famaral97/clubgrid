import random

from sqlalchemy import desc

import src.adapters.sql.grids as grids_adapter
from src.models.condition import Condition
from src.models.grid import Grid
from src.models.grid_type import GridType
from datetime import datetime, timedelta

from src.models.tag_exclusion import TagExclusion


def generate_grid(
        app,
        grid_type_id,
        max_clubs_per_cell=30,
        max_common_conditions=2,
        previous_grids_number=3
):
    grid_type = GridType.query.get(grid_type_id)
    min_clubs_per_cell = 5 if grid_type.id == 1 else 1

    row_conditions, column_conditions = _generate_grid_with_conditions(
        min_clubs_per_cell, max_clubs_per_cell, max_common_conditions,
        previous_grids_number, grid_type, app)

    insert_grid(app, row_conditions, column_conditions, grid_type)

    ids = []
    for row_cond in row_conditions:
        ids.append(row_cond.id)
    for column_cond in column_conditions:
        ids.append(column_cond.id)
    return ids


def insert_grid(app, row_conditions, column_conditions, grid_type):
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

    grids_adapter.insert_without_id(new_grid, app)


def _generate_grid_with_conditions(
        min_clubs_per_cell,
        max_clubs_per_cell,
        max_common_conditions,
        previous_grids_number,
        grid_type,
        app
):
    conditions_query = Condition.query.filter(Condition.deprecated.is_(False))
    excluding_tags = TagExclusion.query.filter(TagExclusion.grid_type_id == grid_type.id).all()

    if len(excluding_tags) > 0:
        conditions_query = conditions_query.filter(
            Condition.tag.notin_([excluding_tag.tag for excluding_tag in excluding_tags])
        )

    all_conditions = conditions_query.all()

    all_grids = Grid.query.filter_by(type_id=grid_type.id).order_by(desc(Grid.id)).all()

    conditions_weights = _compute_weights(all_conditions, all_grids)

    grid_attempt = 0

    while True:
        grid_attempt += 1
        print("Creating grid: attempt #", grid_attempt, flush=True)

        conditions_sample = _get_weighted_sample_of_conditions(all_conditions, conditions_weights)

        row_conditions = conditions_sample[:3]
        col_conditions = conditions_sample[3:]

        grid_solution = grids_adapter.get_solutions(row_conditions, col_conditions, grid_type, app)

        if _grid_has_enough_solutions(grid_solution, min_clubs_per_cell, max_clubs_per_cell):
            if _grid_is_completable(grid_solution):
                if _grid_is_different_enough(conditions_sample, all_grids, previous_grids_number,
                                             max_common_conditions):
                    print("--- ✅ SUCCESS!", flush=True)
                    return row_conditions, col_conditions
                else:
                    print("--- 🟰❌ not different enough", flush=True)
            else:
                print("--- 📋❌ not completable", flush=True)
        else:
            print("--- 🤏❌ not enough solutions", flush=True)


def _get_weighted_sample_of_conditions(conditions, weights):
    selected_conditions = []

    while len(selected_conditions) < 6:
        random_condition = random.choices(conditions, weights=weights)[0]
        if random_condition not in selected_conditions:
            selected_conditions.append(random_condition)
    return selected_conditions


def _compute_weights(conditions, grids):
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


def _grid_is_different_enough(conditions_sample, all_grids, previous_grids_number, max_common_conditions):
    if grid_has_different_conditions_than_previous_grids(conditions_sample, all_grids, previous_grids_number) and \
            grid_is_not_too_similar(conditions_sample, all_grids, max_common_conditions) and \
            grid_has_different_conditions_tags(conditions_sample):
        return True


def grid_has_different_conditions_tags(conditions):
    tags = [condition.tag for condition in conditions]
    return len(set(tags)) == 6


def grid_has_different_conditions_than_previous_grids(conditions, grids, n_grids):
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


def grid_is_not_too_similar(conditions, grids, max_conditions_number):
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


def _grid_has_enough_solutions(grid, min_clubs_per_cell, max_clubs_per_cell):
    for row in grid:
        for cell in row:
            if len(cell) < min_clubs_per_cell or len(cell) > max_clubs_per_cell:
                return False

    return True


def _grid_is_completable(grid):
    def backtrack(used, row, col):
        if row == 3:
            return True

        next_row, next_col = (row, col + 1) if col < 2 else (row + 1, 0)

        for club in grid[row][col]:
            if club not in used:
                used.add(club)
                if backtrack(used, next_row, next_col):
                    return True
                used.remove(club)

        return False

    return backtrack(set(), 0, 0)
