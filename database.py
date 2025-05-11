import csv
from datetime import datetime, timedelta

import yaml
from sqlalchemy import text, inspect, desc
from sqlalchemy.dialects.mysql import insert

from models import Condition, Club, Grid, Answer, GridType


def load_conditions(db, app):
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

    with app.app_context():
        stmt = insert(Condition).values([to_dict(condition) for condition in all_conditions])
        stmt = stmt.on_duplicate_key_update(stmt.inserted)
        db.session.execute(stmt)
        db.session.commit()


def load_grid_types(db, app):
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

    with app.app_context():
        stmt = insert(GridType).values([to_dict(grid_type) for grid_type in all_grid_types])
        stmt = stmt.on_duplicate_key_update(stmt.inserted)
        db.session.execute(stmt)
        db.session.commit()


def create_default_grids(db, app):
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



    with app.app_context():
        stmt = insert(Grid).values([to_dict(grid) for grid in grids])
        stmt = stmt.on_duplicate_key_update(stmt.inserted)

        db.session.execute(stmt)

        db.session.commit()


def load_clubs(db, app):
    all_clubs = []

    with open('./data/data.csv') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',')

        for club_row in csvreader:
            name = club_row["name"]
            league = club_row["league_2024_25"]
            all_clubs.append(
                Club(
                    id=club_row["id"],
                    name=club_row['name'],
                    logo=f"https://github.com/Famaral97/clubgrid/blob/main/data/logos/{league}/{name}.png?raw=true".replace(
                        " ", "%20"),
                    country=club_row['country'],

                    name_has_number=club_row['name_has_number'] == "YES",
                    logo_has_animal=club_row['logo_has_animal'] == "YES",
                    logo_has_winged_animal=club_row['logo_has_winged_animal'] == "YES",
                    logo_has_person=club_row['logo_has_person'] == "YES",
                    logo_has_football=club_row['logo_has_football'] == "YES",
                    logo_is_circular=club_row['logo_is_circular'] == "YES",
                    logo_has_crown=club_row['logo_has_crown'] == "YES",
                    logo_has_numbers=club_row['logo_has_numbers'] == "YES",
                    num_stars_in_logo=club_row['num_stars_in_logo'],

                    num_colors_in_logo=club_row['num_colors_in_logo'],
                    logo_has_red=club_row['logo_has_red'] == "YES",
                    logo_has_blue=club_row['logo_has_blue'] == "YES",
                    logo_has_green=club_row['logo_has_green'] == "YES",
                    logo_has_black=club_row['logo_has_black'] == "YES",

                    in_capital=club_row['in_capital'] == "YES",

                    league_titles=club_row['league_titles'],
                    league_2024_25=club_row['league_2024_25'],
                    league_2023_24=club_row['league_2023_24'],
                    league_2022_23=club_row['league_2022_23'],

                    domestic_cup_titles=club_row['domestic_cup_titles'],
                    domestic_cup_runner_up=club_row['domestic_cup_runner_up'],

                    domestic_supercup_titles=club_row['domestic_supercup_titles'],
                    domestic_supercup_runner_up=club_row['domestic_supercup_runner_up'],

                    champions_league_2024_25=club_row['champions_league_2024_25'] == "YES",
                    champions_league_titles=club_row['champions_league_titles'],
                    champions_league_runner_up=club_row['champions_league_runner_up'],

                    europa_league_2024_25=club_row['europa_league_2024_25'] == "YES",
                    europa_league_titles=club_row['europa_league_titles'],
                    europa_league_runner_up=club_row['europa_league_runner_up'],

                    cups_winners_cup_titles=club_row['cups_winners_cup_titles'],
                    cups_winners_cup_runner_up=club_row['cups_winners_cup_runner_up'],

                    uefa_super_cup_titles=club_row['uefa_super_cup_titles'],
                    uefa_super_cup_runner_up=club_row['uefa_super_cup_runner_up'],

                    club_world_cup_titles=club_row['club_world_cup_titles'],
                    club_world_cup_runner_up=club_row['club_world_cup_runner_up'],

                    best_club_awards=club_row['best_club_awards'],
                    best_club_runner_up=club_row['best_club_runner_up'],
                    best_club_third_place=club_row['best_club_third_place'],

                    instagram_followers=club_row['instagram_followers'],

                    legal_name=club_row['legal_name'],
                    foundation_year=club_row['foundation_year'],

                    most_valuable_player=club_row['most_valuable_player'],
                    oldest_player=club_row['oldest_player'],
                    most_expensive_entry=club_row['most_expensive_entry'],
                    most_expensive_exit=club_row['most_expensive_exit'],
                    squad_size=club_row['squad_size'],
                    average_age=club_row['average_age'],
                    foreigners_count=club_row['foreigners_count'],
                    foreigners_percentage=club_row['foreigners_percentage'],
                    national_team_players=club_row['national_team_players'],
                    stadium_name=club_row['stadium_name'],
                    stadium_capacity=club_row['stadium_capacity'],
                    total_market_value=club_row['total_market_value']
                )
            )

    with app.app_context():
        stmt = insert(Club).values([to_dict(club) for club in all_clubs])
        stmt = stmt.on_duplicate_key_update(stmt.inserted)
        db.session.execute(stmt)
        db.session.commit()


def get_grid_answers(grid, app):
    with app.app_context():
        grid_type_id = grid.type_id if grid.type_id else 1
        grid_type = GridType.query.get(grid_type_id)

    grid_answers = []
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_1, grid.row_condition_1, grid_type, app))
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_1, grid.row_condition_2, grid_type, app))
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_1, grid.row_condition_3, grid_type, app))
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_2, grid.row_condition_1, grid_type, app))
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_2, grid.row_condition_2, grid_type, app))
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_2, grid.row_condition_3, grid_type, app))
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_3, grid.row_condition_1, grid_type, app))
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_3, grid.row_condition_2, grid_type, app))
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_3, grid.row_condition_3, grid_type, app))
    return grid_answers


def get_cell_answers(grid, column_condition_id, row_condition_id, grid_type, app):
    with app.app_context():
        query = Club.query.filter(
            text(Condition.query.get(row_condition_id).expression),
            text(Condition.query.get(column_condition_id).expression)
        )

        if grid_type is not None:
            query = query.filter(text(grid_type.expression))

        solution_clubs = query.all()

    return [Answer(
        grid_id=grid.id,
        column_condition_id=column_condition_id,
        row_condition_id=row_condition_id,
        club_id=club.id,
        is_solution=True,
        count=0,
    ) for club in solution_clubs]


def get_grid_solution(row_conditions, column_conditions, grid_type, app):
    return [
        [
            get_cell_solution(row_conditions[0], column_conditions[0], grid_type, app),
            get_cell_solution(row_conditions[0], column_conditions[1], grid_type, app),
            get_cell_solution(row_conditions[0], column_conditions[2], grid_type, app)
        ],
        [
            get_cell_solution(row_conditions[1], column_conditions[0], grid_type, app),
            get_cell_solution(row_conditions[1], column_conditions[1], grid_type, app),
            get_cell_solution(row_conditions[1], column_conditions[2], grid_type, app)
        ],
        [
            get_cell_solution(row_conditions[2], column_conditions[0], grid_type, app),
            get_cell_solution(row_conditions[2], column_conditions[1], grid_type, app),
            get_cell_solution(row_conditions[2], column_conditions[2], grid_type, app)
        ]
    ]


def get_cell_solution(row_condition, col_condition, grid_type, app):
    with app.app_context():
        query = Club.query.filter(text(row_condition.expression), text(col_condition.expression))

        if grid_type is not None:
            query = query.filter(text(grid_type.expression))

        solution_clubs = query.all()

    return solution_clubs


def insert_grid(db, app, row_conditions, column_conditions, grid_type):
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

    with app.app_context():
        stmt = insert(Grid).values(to_dict(new_grid))
        result = db.session.execute(stmt)
        db.session.commit()

        new_grid.id = result.lastrowid

        db.session.commit()


def to_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


def to_int(s):
    s = s.replace('€', '')

    if '+-0' in s:
        return 0

    if s[-1] == 'm':
        multiplier = 1_000_000
    elif s[-1] == 'k':
        multiplier = 1_000
    else:
        raise ValueError("Invalid suffix. Only 'm' and 'k' are supported.")

    numeric_part = float(s[:-1])

    return int(numeric_part * multiplier)
