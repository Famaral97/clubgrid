import src.adapters.sql.conditions as conditions_adapter
import src.adapters.sql.grids as grids_adapter

from src.models.grid import Grid
from src.models.grid_type import GridType


def get_grid_solution(grid_id, app):
    grid = Grid.query.get(grid_id)
    grid_type = GridType.query.get(grid.type_id)

    solutions = grids_adapter.get_solutions_with_answers(grid, grid_type, app)

    conditions = conditions_adapter.get_for_grid(grid)

    return solutions, conditions
