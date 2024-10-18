import csv

from sqlalchemy import text, inspect
from sqlalchemy.dialects.mysql import insert

from models import Condition, Club, Grid, Answer


def create_default_conditions(db, app):
    conditions = [
        Condition(id=1, description="Logo has animal", expression="clubs.has_animal = True"),
        Condition(id=2, description="Logo doesn't have animal", expression="clubs.has_animal = False"),

        Condition(id=3, description="In Premier League", expression="clubs.league_2024_25 = 'EN1'"),
        Condition(id=4, description="In La Liga", expression="clubs.league_2024_25 = 'ES1'"),
        Condition(id=5, description="In Liga Portugal", expression="clubs.league_2024_25 = 'PT1'"),
        Condition(id=6, description="In Ligue 1", expression="clubs.league_2024_25 = 'FR1'"),
        Condition(id=7, description="In Bundesliga", expression="clubs.league_2024_25 = 'DE1'"),
        Condition(id=8, description="In Italian Serie A", expression="clubs.league_2024_25 = 'IT1'"),

        Condition(id=9, description="Logo has winged animal", expression="clubs.has_winged_animal = True"),
        Condition(id=10, description="Logo doesn't have winged animal", expression="clubs.has_winged_animal = False"),

        Condition(id=11, description="Logo has person", expression="clubs.has_person = True"),
        Condition(id=12, description="Logo doesn't have person", expression="clubs.has_person = False"),

        Condition(id=13, description="Logo has a football", expression="clubs.has_football = True"),
        Condition(id=14, description="Logo doesn't a football", expression="clubs.has_football = False"),

        Condition(id=15, description="Logo doesn't have stars", expression="clubs.stars_number = 0"),
        Condition(id=16, description="Logo has stars", expression="clubs.stars_number != 0"),

        Condition(id=17, description="Logo has exactly 1 or 2 colors",
                  expression="(clubs.colors_number = '1' or clubs.colors_number = '2')"),
        Condition(id=18, description="Logo has exactly 3 colors", expression="clubs.colors_number = '3'"),
        Condition(id=19, description="Logo has 4 or more colors", expression="clubs.colors_number = '4+'"),

        Condition(id=20, description="Logo has numbers", expression="clubs.has_numbers = True"),
        Condition(id=21, description="Logo doesn't have numbers", expression="clubs.has_numbers = False"),

        Condition(id=22, description="Logo has red", expression="clubs.has_color_red = True"),
        Condition(id=23, description="Logo doesn't have red", expression="clubs.has_color_red = False"),

        Condition(id=24, description="Logo has blue", expression="clubs.has_color_blue = True"),
        Condition(id=25, description="Logo doesn't have blue", expression="clubs.has_color_blue = False"),

        Condition(id=26, description="Logo has green", expression="clubs.has_color_green = True"),
        Condition(id=27, description="Logo doesn't have green", expression="clubs.has_color_green = False"),

        Condition(id=28, description="Has at least 1 league title", expression="clubs.league_titles > 0"),
        Condition(id=29, description="Never won a league title", expression="clubs.league_titles = 0"),

        Condition(id=30, description="Logo has crown", expression="clubs.has_crown = True"),
        Condition(id=31, description="Logo doesn't have crown", expression="clubs.has_crown = False"),

        Condition(id=32, description="Never won UEFA Champions League / European Cup",
                  expression="clubs.champions_league_titles = 0"),
        Condition(id=33, description="Won UEFA Champions League / European Cup",
                  expression="clubs.champions_league_titles > 0"),
        Condition(id=34, description="Was UEFA Champions League / European Cup Runner-Up",
                  expression="clubs.champions_league_runner_up > 0"),
        Condition(id=35, description="Was in UEFA Champions League / European Cup Final",
                  expression="(clubs.champions_league_titles > 0 or clubs.champions_league_runner_up > 0)"),

        Condition(id=36, description="Never won UEFA Europa League / UEFA Cup",
                  expression="clubs.europa_league_titles = 0"),
        Condition(id=37, description="Won UEFA Europa League / UEFA Cup",
                  expression="clubs.europa_league_titles > 0"),
        Condition(id=38, description="Was UEFA Europa League / UEFA Cup Runner-Up",
                  expression="clubs.europa_league_runner_up > 0"),
        Condition(id=39, description="Was in UEFA Europa League / UEFA Cup Final",
                  expression="(clubs.europa_league_titles > 0 or clubs.europa_league_runner_up > 0)"),

        Condition(id=40, description="Based in a capital city", expression="clubs.in_capital = True"),
        Condition(id=41, description="Not based in a capital", expression="clubs.in_capital = False"),

        Condition(id=42, description="Name starts with A, B or C",
                  expression="(clubs.name like 'a%' or clubs.name like 'b%' or clubs.name like 'c%')"),
        Condition(id=43, description="Name starts with R or S",
                  expression="(clubs.name like 'r%' or clubs.name like 's%')"),
        Condition(id=69, description="Name starts with D, E, F or G",
                  expression="(clubs.name like 'd%' or clubs.name like 'e%'"
                             " or clubs.name like 'f%' or clubs.name like 'g%')"),
        Condition(id=70, description="Name starts with L, M, N, O or P",
                  expression="(clubs.name like 'l%' or clubs.name like 'm%' or clubs.name like 'n%'"
                             " or clubs.name like 'o%' or clubs.name like 'p%')"),
        Condition(id=71, description="Name starts with T, U or V",
                  expression="(clubs.name like 't%' or clubs.name like 'u%' or clubs.name like 'v%')"),
        Condition(id=72, description="Name has a number", expression="clubs.name_has_number = True"),
        Condition(id=73, description="Name does not have a number", expression="clubs.name_has_number = False"),

        Condition(id=78, description="Name ends with A", expression="clubs.name like '%a'"),
        Condition(id=79, description="Name ends with B", expression="clubs.name like '%b'"),
        Condition(id=80, description="Name ends with E", expression="clubs.name like '%e'"),

        Condition(id=44, description="Logo is circular", expression="clubs.is_circular = True"),

        Condition(id=45, description="Never won a domestic Cup", expression="clubs.cup_titles = 0"),
        Condition(id=46, description="Never a domestic Cup finalist",
                  expression="(clubs.cup_titles = 0 and clubs.cup_runner_up = 0)"),
        Condition(id=47, description="Won a domestic Cup", expression="clubs.cup_titles > 0"),
        Condition(id=48, description="Won domestic Cup 5 or more times", expression="clubs.cup_titles >= 5"),
        Condition(id=49, description="Domestic Cup finalist but never won",
                  expression="(clubs.cup_titles = 0 and clubs.cup_runner_up > 0)"),

        Condition(id=50, description="Logo has black", expression="clubs.has_color_black = True"),
        Condition(id=51, description="Logo doesn't have black", expression="clubs.has_color_black = False"),

        Condition(id=52, description="Stadium capacity under 20k", expression="clubs.stadium_capacity < 20000"),
        Condition(id=53, description="Stadium capacity over 50k", expression="clubs.stadium_capacity > 50000"),
        Condition(id=54, description="Stadium capacity between 20k and 50k",
                  expression="clubs.stadium_capacity between 20000 and 50000"),

        Condition(id=55, description="Squad size fewer than 25 players", expression="clubs.squad_size <= 24"),
        Condition(id=56, description="Squad size more than 29 players ", expression="clubs.squad_size >= 30"),

        Condition(id=57, description="Squad average age at most 25y", expression="clubs.average_age <= 25"),
        Condition(id=58, description="Squad average age at least 27y", expression="clubs.average_age >= 27"),

        Condition(id=59, description="Squad has fewer than 13 foreigners", expression="clubs.foreigners_number < 13"),
        Condition(id=60, description="Squad has at least 20 foreigners", expression="clubs.foreigners_number >= 20"),

        Condition(id=61, description="Squad composed by less than 50% foreigners",
                  expression="clubs.foreigners_percentage < 50"),
        Condition(id=62, description="Squad composed by more than 70% foreigners",
                  expression="clubs.foreigners_percentage > 70"),

        Condition(id=63, description="Squad has fewer than 6 national team players",
                  expression="clubs.national_team_players < 6"),
        Condition(id=64, description="Squad has at least 14 national team players",
                  expression="clubs.national_team_players >= 14"),

        Condition(id=65, description="Positive net transfer record", expression="clubs.net_transfer_record > 0"),
        Condition(id=66, description="Net transfer record over +20M euros",
                  expression="clubs.net_transfer_record > 20000000"),
        Condition(id=67, description="Negative net transfer record", expression="clubs.net_transfer_record < 0"),
        Condition(id=68, description="Net transfer record under -30M euros",
                  expression="clubs.net_transfer_record < 30000000"),

        Condition(id=74, description="Founded in the 19th century", expression="clubs.year_founded < 1901"),
        Condition(id=75, description="Founded before 1890", expression="clubs.year_founded < 1890"),
        Condition(id=76, description="Founded after 1930", expression="clubs.year_founded > 1930"),

        Condition(id=77, description="Has played in 2nd tier in the last 2 seasons",
                  expression="(clubs.league_2023_24 in ('IT2', 'PT2', 'EN2', 'ES2', 'FR2', 'DE2') or "
                             "clubs.league_2022_23 in ('IT2', 'PT2', 'EN2', 'ES2', 'FR2', 'DE2')) "),

        # next available condition id: 81
    ]

    with app.app_context():
        stmt = insert(Condition).values([to_dict(condition) for condition in conditions])
        stmt = stmt.on_duplicate_key_update(stmt.inserted)
        db.session.execute(stmt)
        db.session.commit()


def create_default_grids(db, app):
    grids = [
        Grid(
            id=5,
            row_condition_1=5,
            row_condition_2=23,
            row_condition_3=24,
            column_condition_1=72,
            column_condition_2=73,
            column_condition_3=43,
        ),
        Grid(
            id=4,
            row_condition_1=32,
            row_condition_2=22,
            row_condition_3=7,
            column_condition_1=15,
            column_condition_2=25,
            column_condition_3=9,
        ),
        Grid(
            id=3,
            row_condition_1=1,
            row_condition_2=3,
            row_condition_3=17,
            column_condition_1=20,
            column_condition_2=28,
            column_condition_3=42,
        ),
        Grid(
            id=2,
            row_condition_1=30,
            row_condition_2=13,
            row_condition_3=16,
            column_condition_1=10,
            column_condition_2=19,
            column_condition_3=41,
        ),
        Grid(
            id=1,
            row_condition_1=11,
            row_condition_2=26,
            row_condition_3=28,
            column_condition_1=33,
            column_condition_2=39,
            column_condition_3=40,
        )
    ]

    answers = []
    for grid in grids:
        answers.extend(get_answers(grid, grid.column_condition_1, grid.row_condition_1, app))
        answers.extend(get_answers(grid, grid.column_condition_1, grid.row_condition_2, app))
        answers.extend(get_answers(grid, grid.column_condition_1, grid.row_condition_3, app))
        answers.extend(get_answers(grid, grid.column_condition_2, grid.row_condition_1, app))
        answers.extend(get_answers(grid, grid.column_condition_2, grid.row_condition_2, app))
        answers.extend(get_answers(grid, grid.column_condition_2, grid.row_condition_3, app))
        answers.extend(get_answers(grid, grid.column_condition_3, grid.row_condition_1, app))
        answers.extend(get_answers(grid, grid.column_condition_3, grid.row_condition_2, app))
        answers.extend(get_answers(grid, grid.column_condition_3, grid.row_condition_3, app))

    with app.app_context():
        stmt = insert(Grid).values([to_dict(grid) for grid in grids])
        stmt = stmt.on_duplicate_key_update(stmt.inserted)
        db.session.execute(stmt)

        stmt = insert(Answer).values([to_dict(answer) for answer in answers])
        stmt = stmt.on_duplicate_key_update(grid_id=stmt.inserted.grid_id)  # ignore update
        db.session.execute(stmt)

        db.session.commit()


def get_answers(grid, column_condition_id, row_condition_id, app):
    with app.app_context():
        row_condition_expression = Condition.query.get(column_condition_id).expression
        column_condition_expression = Condition.query.get(row_condition_id).expression

        solution_clubs = Club.query.filter(
            text(row_condition_expression),
            text(column_condition_expression)).all()

    return [Answer(
        grid_id=grid.id,
        column_condition_id=column_condition_id,
        row_condition_id=row_condition_id,
        club_id=club.id,
        is_solution=True,
        count=0,
    ) for club in solution_clubs]


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
                    has_crown=club_row["logo_has_crown"] == "YES",
                    champions_league_titles=club_row["champions_league_titles"],
                    champions_league_runner_up=club_row["champions_league_runner-up"],
                    europa_league_titles=club_row["europa_league_titles"],
                    europa_league_runner_up=club_row["europa_league_runner-up"],
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
                )
            )

    return clubs


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
