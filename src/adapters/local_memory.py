from datetime import datetime

from src.models.grid import Grid

grids = [
    Grid(
        id=1,
        type_id=1,
        local_id=1,
        starting_date=datetime(2024, 12, 5, 0, 0),
        row_condition_1=1,
        row_condition_2=2,
        row_condition_3=3,
        column_condition_1=4,
        column_condition_2=5,
        column_condition_3=6,
    )
]