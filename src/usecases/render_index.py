from datetime import datetime

import src.adapters.sql.conditions as conditions_adapter
from src.models.UnauthorizedGridException import UnauthorizedGridException
from src.models.grid import Grid
from src.models.grid_type import GridType


def render_index(grid_id):
    grid = Grid.query.get(grid_id)

    if grid is None or grid.starting_date > datetime.now():
        raise UnauthorizedGridException()

    grid_type = GridType.query.get(grid.type_id)

    conditions = conditions_adapter.get_for_grid(grid)

    return grid, grid_type, conditions
