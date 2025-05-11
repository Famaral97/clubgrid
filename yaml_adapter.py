import yaml

from models import Condition, GridType


def load_conditions():
    with open('./data/conditions.yaml', 'r', encoding='utf-8') as file:
        conditions_data = yaml.safe_load(file)

    all_conditions = []
    for tag, conditions in conditions_data.items():
        for condition in conditions:
            all_conditions.append(
                Condition(
                    id=condition['id'],
                    description=condition['description'],
                    expression=condition['expression'],
                    tags=tag,
                    deprecated=False
                )
            )

    return all_conditions


def load_grid_types():
    with open('./data/grid_types.yaml', 'r', encoding='utf-8') as file:
        grid_types_data = yaml.safe_load(file)

    all_grid_types = []
    for grid_type in grid_types_data:
        all_grid_types.append(
            GridType(
                id=grid_type['id'],
                description=grid_type['description'],
                expression=grid_type['expression'],
                exclude_country_conditions=grid_type['exclude_country_conditions'],
            )
        )

    return all_grid_types
