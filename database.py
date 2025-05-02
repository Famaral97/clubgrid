import csv
from datetime import datetime, timedelta

from sqlalchemy import text, inspect, desc
from sqlalchemy.dialects.mysql import insert

from models import Condition, Club, Grid, Answer, GridType


def create_default_conditions(db, app):
    conditions = [
        Condition(id=1, description="Logo has animal", expression="clubs.has_animal = True", tags="logo-items"),
        Condition(id=2, description="Logo doesn't have animal", expression="clubs.has_animal = False", tags="logo-items"),

        Condition(id=3, description="In Premier League", expression="clubs.league_2024_25 = 'EN1'", tags="league"),
        Condition(id=4, description="In La Liga", expression="clubs.league_2024_25 = 'ES1'", tags="league"),
        Condition(id=5, description="In Liga Portugal", expression="clubs.league_2024_25 = 'PT1'", tags="league"),
        Condition(id=6, description="In Ligue 1", expression="clubs.league_2024_25 = 'FR1'", tags="league"),
        Condition(id=7, description="In Bundesliga", expression="clubs.league_2024_25 = 'DE1'", tags="league"),
        Condition(id=8, description="In Italian Serie A", expression="clubs.league_2024_25 = 'IT1'", tags="league"),

        Condition(id=9, description="Logo has winged animal", expression="clubs.has_winged_animal = True", tags="logo-items"),
        Condition(id=10, description="Logo doesn't have winged animal", expression="clubs.has_winged_animal = False", tags="logo-items"),

        Condition(id=11, description="Logo has person", expression="clubs.has_person = True", tags="logo-items"),
        Condition(id=12, description="Logo doesn't have person", expression="clubs.has_person = False", tags="logo-items"),

        Condition(id=13, description="Logo has a football", expression="clubs.has_football = True", tags="logo-items"),
        Condition(id=14, description="Logo doesn't a football", expression="clubs.has_football = False", tags="logo-items"),

        Condition(id=15, description="Logo doesn't have stars", expression="clubs.stars_number = 0", tags="logo-items"),
        Condition(id=16, description="Logo has stars", expression="clubs.stars_number != 0", tags="logo-items"),

        Condition(id=17, description="Logo has exactly 1 or 2 colors",
                  expression="(clubs.colors_number = '1' or clubs.colors_number = '2')", tags="logo-colors"),
        Condition(id=18, description="Logo has exactly 3 colors", expression="clubs.colors_number = '3'", tags="logo-colors"),
        Condition(id=19, description="Logo has 4 or more colors", expression="clubs.colors_number = '4+'", tags="logo-colors"),

        Condition(id=20, description="Logo has numbers", expression="clubs.has_numbers = True", tags="logo-items"),
        Condition(id=21, description="Logo doesn't have numbers", expression="clubs.has_numbers = False", tags="logo-items"),

        Condition(id=22, description="Logo has red", expression="clubs.has_color_red = True", tags="logo-colors"),
        Condition(id=23, description="Logo doesn't have red", expression="clubs.has_color_red = False", tags="logo-colors"),

        Condition(id=24, description="Logo has blue", expression="clubs.has_color_blue = True", tags="logo-colors"),
        Condition(id=25, description="Logo doesn't have blue", expression="clubs.has_color_blue = False", tags="logo-colors"),

        Condition(id=26, description="Logo has green", expression="clubs.has_color_green = True", tags="logo-colors"),
        Condition(id=27, description="Logo doesn't have green", expression="clubs.has_color_green = False", tags="logo-colors"),

        Condition(id=81, description="Has at least 5 league titles", expression="clubs.league_titles > 4", tags="titles-domestic"),
        Condition(id=28, description="Has at least 1 league title", expression="clubs.league_titles > 0", tags="titles-domestic"),
        Condition(id=29, description="Never won a league title", expression="clubs.league_titles = 0", tags="titles-domestic"),

        Condition(id=30, description="Logo has crown", expression="clubs.has_crown = True", tags="logo-items"),
        Condition(id=31, description="Logo doesn't have crown", expression="clubs.has_crown = False", tags="logo-items"),

        Condition(id=32, description="Never won UEFA Champions League / European Cup",
                  expression="clubs.champions_league_titles = 0", tags="titles-uefa"),
        Condition(id=33, description="Won UEFA Champions League / European Cup",
                  expression="clubs.champions_league_titles > 0", tags="titles-uefa"),
        Condition(id=34, description="Was UEFA Champions League / European Cup Runner-Up",
                  expression="clubs.champions_league_runner_up > 0", tags="titles-uefa"),
        Condition(id=35, description="Was in UEFA Champions League / European Cup Final",
                  expression="(clubs.champions_league_titles > 0 or clubs.champions_league_runner_up > 0)", tags="titles-uefa"),

        Condition(id=36, description="Never won UEFA Europa League / UEFA Cup",
                  expression="clubs.europa_league_titles = 0", tags="titles-uefa"),
        Condition(id=37, description="Won UEFA Europa League / UEFA Cup",
                  expression="clubs.europa_league_titles > 0", tags="titles-uefa"),
        Condition(id=38, description="Was UEFA Europa League / UEFA Cup Runner-Up",
                  expression="clubs.europa_league_runner_up > 0", tags="titles-uefa"),
        Condition(id=39, description="Was in UEFA Europa League / UEFA Cup Final",
                  expression="(clubs.europa_league_titles > 0 or clubs.europa_league_runner_up > 0)", tags="titles-uefa"),

        Condition(id=40, description="Based in a capital city", expression="clubs.in_capital = True", tags="city"),
        Condition(id=41, description="Not based in a capital", expression="clubs.in_capital = False", tags="city"),

        Condition(id=42, description="Name starts with A, B or C",
                  expression="(clubs.name like 'a%' or clubs.name like 'b%' or clubs.name like 'c%')", tags="name"),
        Condition(id=43, description="Name starts with R or S",
                  expression="(clubs.name like 'r%' or clubs.name like 's%')", tags="name"),
        Condition(id=69, description="Name starts with D, E, F or G",
                  expression="(clubs.name like 'd%' or clubs.name like 'e%'"
                             " or clubs.name like 'f%' or clubs.name like 'g%')", tags="name"),
        Condition(id=70, description="Name starts with L, M, N, O or P",
                  expression="(clubs.name like 'l%' or clubs.name like 'm%' or clubs.name like 'n%'"
                             " or clubs.name like 'o%' or clubs.name like 'p%')", tags="name"),
        Condition(id=71, description="Name starts with T, U or V",
                  expression="(clubs.name like 't%' or clubs.name like 'u%' or clubs.name like 'v%')", tags="name"),
        Condition(id=72, description="Name has a number", expression="clubs.name_has_number = True", tags="name"),
        Condition(id=73, description="Name does not have a number", expression="clubs.name_has_number = False", tags="name"),

        Condition(id=78, description="Name ends with A", expression="clubs.name like '%a'", tags="name"),
        Condition(id=79, description="Name ends with B", expression="clubs.name like '%b'", tags="name"),
        Condition(id=80, description="Name ends with E", expression="clubs.name like '%e'", tags="name"),

        Condition(id=44, description="Logo is circular", expression="clubs.is_circular = True", tags="logo-items"),

        Condition(id=45, description="Never won a domestic Cup", expression="clubs.cup_titles = 0", tags="titles-domestic"),
        Condition(id=46, description="Never a domestic Cup finalist",
                  expression="(clubs.cup_titles = 0 and clubs.cup_runner_up = 0)", tags="titles-domestic"),
        Condition(id=47, description="Won a domestic Cup", expression="clubs.cup_titles > 0", tags="titles-domestic"),
        Condition(id=48, description="Won domestic Cup 5 or more times", expression="clubs.cup_titles >= 5", tags="titles-domestic"),
        Condition(id=49, description="Domestic Cup finalist but never won",
                  expression="(clubs.cup_titles = 0 and clubs.cup_runner_up > 0)", tags="titles-domestic"),

        Condition(id=50, description="Logo has black", expression="clubs.has_color_black = True", tags="logo-colors"),
        Condition(id=51, description="Logo doesn't have black", expression="clubs.has_color_black = False", tags="logo-colors"),

        Condition(id=52, description="Stadium capacity under 20k", expression="clubs.stadium_capacity < 20000", tags="stadium"),
        Condition(id=53, description="Stadium capacity over 50k", expression="clubs.stadium_capacity > 50000", tags="stadium"),
        Condition(id=54, description="Stadium capacity between 20k and 50k",
                  expression="clubs.stadium_capacity between 20000 and 50000", tags="stadium"),

        Condition(id=55, description="Squad size fewer than 25 players", expression="clubs.squad_size <= 24", tags="squad"),
        Condition(id=56, description="Squad size more than 29 players ", expression="clubs.squad_size >= 30", tags="squad"),

        Condition(id=57, description="Squad average age at most 25y", expression="clubs.average_age <= 25", tags="squad"),
        Condition(id=58, description="Squad average age at least 27y", expression="clubs.average_age >= 27", tags="squad"),

        Condition(id=59, description="Squad has fewer than 13 foreigners", expression="clubs.foreigners_number < 13", tags="squad"),
        Condition(id=60, description="Squad has at least 20 foreigners", expression="clubs.foreigners_number >= 20", tags="squad"),

        Condition(id=61, description="Squad with under 50% foreign players",
                  expression="clubs.foreigners_percentage < 50", tags="squad"),
        Condition(id=62, description="Squad with over 70% foreign players",
                  expression="clubs.foreigners_percentage > 70", tags="squad"),

        Condition(id=63, description="Squad has fewer than 6 national team players",
                  expression="clubs.national_team_players < 6", tags="squad"),
        Condition(id=64, description="Squad has at least 14 national team players",
                  expression="clubs.national_team_players >= 14", tags="squad"),

        Condition(id=65, description="Positive net transfer record", expression="clubs.net_transfer_record > 0", tags="transfers"),
        Condition(id=66, description="Net transfer record over +20M euros",
                  expression="clubs.net_transfer_record > 20000000", tags="transfers"),
        Condition(id=67, description="Negative net transfer record", expression="clubs.net_transfer_record < 0", tags="transfers"),
        Condition(id=68, description="Net transfer record under -30M euros",
                  expression="clubs.net_transfer_record < -30000000", tags="transfers"),

        Condition(id=74, description="Founded in the 19th century", expression="clubs.year_founded < 1901", tags="foundation"),
        Condition(id=75, description="Founded before 1890", expression="clubs.year_founded < 1890", tags="foundation"),
        Condition(id=76, description="Founded after 1930", expression="clubs.year_founded > 1930", tags="foundation"),

        Condition(id=77, description="Was promoted in the last 2 seasons",
                  expression="(clubs.league_2023_24 in ('IT2', 'PT2', 'EN2', 'ES2', 'FR2', 'DE2') or "
                             "clubs.league_2022_23 in ('IT2', 'PT2', 'EN2', 'ES2', 'FR2', 'DE2')) ", tags="promotions"),

        Condition(id=82, description="Never won a domestic Super Cup", expression="clubs.national_supercup_titles = 0",
                  tags="titles-domestic"),
        Condition(id=83, description="Won a domestic Super Cup", expression="clubs.national_supercup_titles > 0",
                  tags="titles-domestic"),
        Condition(id=84, description="Domestic Super Cup finalist but never won",
                  expression="clubs.national_supercup_titles = 0 and clubs.national_supercup_runner_up > 0",
                  tags="titles-domestic"),
        Condition(id=85, description="Never a domestic Super Cup finalist",
                  expression="clubs.national_supercup_titles = 0 and clubs.national_supercup_runner_up = 0",
                  tags="titles-domestic"),
        Condition(id=86, description="Won domestic Super Cup 5 or more times",
                  expression="clubs.national_supercup_titles > 5", tags="titles-domestic"),

        Condition(id=87, description="Never won a Cup Winners' Cup", expression="clubs.cups_winners_cup_titles = 0",
                  tags="titles-uefa"),
        Condition(id=88, description="Won a Cup Winners' Cup", expression="clubs.cups_winners_cup_titles > 0",
                  tags="titles-uefa"),
        Condition(id=89, description="Cup Winners' Cup finalist but never won",
                  expression="clubs.cups_winners_cup_titles = 0 and clubs.cups_winners_cup_runner_up > 0",
                  tags="titles-uefa"),
        Condition(id=90, description="Never a Cup Winners' Cup finalist",
                  expression="clubs.cups_winners_cup_titles = 0 and clubs.cups_winners_cup_runner_up = 0",
                  tags="titles-uefa"),

        Condition(id=91, description="Has at least 10M Instagram followers",
                  expression="clubs.instagram_followers >= 10000000", tags="followers"),
        Condition(id=92, description="Has fewer than 10M Instagram followers",
                  expression="clubs.instagram_followers < 10000000", tags="followers"),

        Condition(id=93, description="Never won a UEFA Super Cup", expression="clubs.uefa_super_cup_titles = 0",
                  tags="titles-uefa"),
        Condition(id=94, description="Won a UEFA Super Cup", expression="clubs.uefa_super_cup_titles > 0",
                  tags="titles-uefa"),
        Condition(id=95, description="UEFA Super Cup finalist but never won",
                  expression="clubs.uefa_super_cup_titles = 0 and clubs.uefa_super_cup_runner_up > 0",
                  tags="titles-uefa"),
        Condition(id=96, description="Never a UEFA Super Cup finalist",
                  expression="clubs.uefa_super_cup_titles = 0 and clubs.uefa_super_cup_runner_up = 0",
                  tags="titles-uefa"),

        Condition(id=97, description="Never won a Club World Cup", expression="clubs.club_world_cup_titles = 0",
                  tags="titles-fifa"),
        Condition(id=98, description="Won a Club World Cup", expression="clubs.club_world_cup_titles > 0",
                  tags="titles-fifa"),
        Condition(id=99, description="Was in a Club World Cup final",
                  expression="(clubs.club_world_cup_titles + clubs.club_world_cup_runner_up) > 0",
                  tags="titles-fifa", deprecated=True),

        Condition(id=100, description="IFFHS Best Club award winner", expression="clubs.best_club_awards > 0",
                  tags="awards"),
        Condition(id=101, description="IFFHS Best Club award runner-up", expression="clubs.best_club_runner_up > 0",
                  tags="awards", deprecated=True),
        Condition(id=102, description="IFFHS Best Club award third place", expression="clubs.best_club_third_place > 0",
                  tags="awards", deprecated=True),
        Condition(id=103, description="Was in the podium of the IFFHS Best Club award",
                  expression="(clubs.best_club_awards + clubs.best_club_runner_up + clubs.best_club_third_place) > 0",
                  tags="awards"),

        Condition(id=104, description="In 2024/25 UEFA Champions League", expression="clubs.champions_league_2024_25 = True",
                  tags="league-continental"),
        Condition(id=105, description="In 2024/25 UEFA Europa League", expression="clubs.europa_league_2024_25 = True",
                  tags="league-continental"),
    ]

    with app.app_context():
        stmt = insert(Condition).values([to_dict(condition) for condition in conditions])
        stmt = stmt.on_duplicate_key_update(stmt.inserted)
        db.session.execute(stmt)
        db.session.commit()


def create_default_grid_types(db, app):
    grid_types = [
        GridType(id=1, description='🏴󠁧󠁢󠁥󠁮󠁧󠁿🇵🇹🇩🇪🇮🇹🇪🇸🇫🇷',
                 expression="clubs.country in ('Italy', 'Portugal', 'England', 'Spain', 'France', 'Germany')"
                 ),
        # GridType(id=2, description='🇵🇹',
        #          expression="clubs.country = 'Portugal'",
        #          exclude_country_conditions=True
        #          ),
        # GridType(id=3, description='🇩🇪',
        #          expression="clubs.country = 'Germany'",
        #          exclude_country_conditions=True
        #          ),
        # GridType(id=4, description='🏴󠁧󠁢󠁥󠁮󠁧󠁿',
        #          expression="clubs.country = 'England'",
        #          exclude_country_conditions=True
        #          ),
        # GridType(id=5, description='🇮🇹',
        #          expression="clubs.country = 'Italy'",
        #          exclude_country_conditions=True
        #          ),
        # GridType(id=6, description='🇪🇸',
        #          expression="clubs.country = 'Spain'",
        #          exclude_country_conditions=True
        #          ),
        # GridType(id=7, description='🇫🇷',
        #          expression="clubs.country = 'France'",
        #          exclude_country_conditions=True
        #          ),
    ]

    with app.app_context():
        stmt = insert(GridType).values([to_dict(grid_type) for grid_type in grid_types])
        stmt = stmt.on_duplicate_key_update(stmt.inserted)
        db.session.execute(stmt)
        db.session.commit()


def create_default_grids(db, app):
    grids = [
        Grid(
            id=1,
            grid_type_id=1,
            local_id=1,
            starting_date=datetime(2024, 12, 5, 0, 0),
            row_condition_1=3,
            row_condition_2=16,
            row_condition_3=103,
            column_condition_1=42,
            column_condition_2=93,
            column_condition_3=92,
        ),
        Grid(
            id=2,
            grid_type_id=2,
            local_id=1,
            starting_date=datetime(2024, 12, 4, 0, 0),
            row_condition_1=54,
            row_condition_2=67,
            row_condition_3=2,
            column_condition_1=60,
            column_condition_2=79,
            column_condition_3=4,
        )
    ]

    answers = []
    for grid in grids:
        answers.extend(get_grid_answers(grid, app))

    with app.app_context():
        stmt = insert(Grid).values([to_dict(grid) for grid in grids])
        stmt = stmt.on_duplicate_key_update(stmt.inserted)

        db.session.execute(stmt)

        stmt = insert(Answer).values([to_dict(answer) for answer in answers])
        stmt = stmt.on_duplicate_key_update(grid_id=stmt.inserted.grid_id)  # ignore update
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


def load_clubs():
    clubs = []

    with open('./data/data.csv') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',')

        for club_row in csvreader:
            short_name = club_row["short_name"]
            country = club_row["Country"]
            league = club_row["2024-25_league"]
            clubs.append(
                Club(
                    id=club_row["id"],
                    name=club_row["name"],
                    short_name=short_name,
                    country=country,
                    logo=f"https://github.com/Famaral97/clubgrid/blob/main/data/logos/{league}/{short_name}.png?raw=true".replace(
                        " ", "%20"),
                    league_2024_25=league,
                    league_2023_24=club_row["2023-24_league"],
                    league_2022_23=club_row["2022-23_league"],
                    year_founded=club_row["year_founded"],
                    name_has_number=club_row["name_has_number"] == "YES",
                    has_animal=club_row["logo_has_animal"] == "YES",
                    has_winged_animal=club_row["logo_has_winged_animal"] == "YES",
                    has_person=club_row["logo_has_person"] == "YES",
                    has_football=club_row["logo_has_ball"] == "YES",
                    stars_number=club_row["#_stars_in_logo"],
                    colors_number=club_row["#_colors_in_logo"],
                    has_numbers=club_row["logo_has_numbers"] == "YES",
                    has_color_red=club_row["logo_has_red"] == "YES",
                    has_color_blue=club_row["logo_has_blue"] == "YES",
                    has_color_green=club_row["logo_has_green"] == "YES",
                    has_color_black=club_row["logo_has_black"] == "YES",
                    league_titles=club_row["league_titles_until_2024"],
                    national_supercup_titles=club_row["domestic_supercup_titles"],
                    national_supercup_runner_up=club_row["domestic_supercup_runner-up"],
                    cups_winners_cup_titles=club_row["cup_winners_cup_titles"],
                    cups_winners_cup_runner_up=club_row["cup_winners_cup_runner-up"],
                    uefa_super_cup_titles=club_row["uefa_super_cup_titles"],
                    uefa_super_cup_runner_up=club_row["uefa_super_cup_runner-up"],
                    club_world_cup_titles=club_row["club_world_cup_titles"],
                    club_world_cup_runner_up=club_row["club_world_cup_runner-up"],
                    has_crown=club_row["logo_has_crown"] == "YES",
                    champions_league_titles=club_row["champions_league_titles"],
                    champions_league_runner_up=club_row["champions_league_runner-up"],
                    europa_league_titles=club_row["europa_league_titles"],
                    europa_league_runner_up=club_row["europa_league_runner-up"],
                    champions_league_2024_25=club_row["champions_league_2024_25"] == "YES",
                    europa_league_2024_25=club_row["europa_league_2024_25"] == "YES",
                    in_capital=club_row["in_a_capital_city"] == "YES",
                    cup_titles=club_row["domestic_cup_titles"],
                    cup_runner_up=club_row["domestic_cup_runner-up"],
                    is_circular=club_row["logo_is_circular"] == "YES",
                    stadium_capacity=club_row["stadium_seats"],
                    squad_size=club_row["squad_size"],
                    average_age=club_row["average_age"],
                    foreigners_number=club_row["foreigners_number"],
                    foreigners_percentage=club_row["foreigners_percentage"],
                    national_team_players=club_row["national_team_players"],
                    net_transfer_record=to_int(club_row["net_transfer_record"]),
                    instagram_followers=club_row["instagram_followers"],
                    best_club_awards=club_row["best_club_awards"],
                    best_club_runner_up=club_row["best_club_runner-up"],
                    best_club_third_place=club_row["best_club_third-place"],
                )
            )

    return clubs


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

        new_grid_answers = get_grid_answers(new_grid, app)

        stmt = insert(Answer).values([to_dict(answer) for answer in new_grid_answers])
        stmt = stmt.on_duplicate_key_update(grid_id=stmt.inserted.grid_id)  # ignore update
        db.session.execute(stmt)

        db.session.commit()


def create_default_clubs(db, app):
    clubs = load_clubs()

    with app.app_context():
        stmt = insert(Club).values([to_dict(club) for club in clubs])
        stmt = stmt.on_duplicate_key_update(stmt.inserted)
        db.session.execute(stmt)
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
