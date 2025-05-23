import yaml

from src.models.condition import Condition
from src.models.grid_type import GridType
from src.models.tag_exclusion import TagExclusion


def load_conditions():
    with open('./data/conditions.yaml', 'r', encoding='utf-8') as file:
        conditions_data = yaml.safe_load(file)

    all_conditions = [
        Condition(
            id=condition['id'],
            description=condition['description'],
            expression=condition['expression'],
            tag=tag,
            deprecated=False
        )
        for tag, conditions in conditions_data.items()
        for condition in conditions
    ]

    return all_conditions


def load_grid_types_and_tag_exclusions():
    with open('./data/grid_types.yaml', 'r', encoding='utf-8') as file:
        grid_types_data = yaml.safe_load(file)

    all_grid_types = [
        GridType(
            id=grid_type['id'],
            description=grid_type['description'],
            expression=grid_type['expression']
        )
        for grid_type in grid_types_data
    ]

    all_tag_exclusions = [
        TagExclusion(
            grid_type_id=grid_type['id'],
            tag=tag
        )
        for grid_type in grid_types_data if 'exclude_tags' in grid_type
        for tag in grid_type['exclude_tags']
    ]

    return all_grid_types, all_tag_exclusions
