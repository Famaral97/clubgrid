import csv

from sqlalchemy import text

from models import Condition, Club, Grid, Answer


def create_default_conditions(db, app):
    conditions = [
        Condition(id=1, description="Logo has animal", expression="clubs.has_animal = True"),
        Condition(id=2, description="Logo doesn't have animal", expression="clubs.has_animal = False"),

        Condition(id=3, description="In Premier League", expression="clubs.league = 'Premier League'"),
        Condition(id=4, description="In La Liga", expression="clubs.league = 'La Liga'"),
        Condition(id=5, description="In Liga Portugal", expression="clubs.league = 'Liga Portugal'"),
        Condition(id=6, description="In Ligue 1", expression="clubs.league = 'Ligue 1'"),
        Condition(id=7, description="In Bundesliga", expression="clubs.league = 'Bundesliga'"),
        Condition(id=8, description="In Italian Serie A", expression="clubs.league = 'Serie A'"),

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

        Condition(id=40, description="Based in capital city", expression="clubs.in_capital = True"),
        Condition(id=41, description="Not based in capital", expression="clubs.in_capital = False"),

        Condition(id=42, description="Name starts with A, B or C",
                  expression="(clubs.name like 'a%' or clubs.name like 'b%' or clubs.name like 'c%')"),
        Condition(id=43, description="Name starts with R or S",
                  expression="(clubs.name like 'r%' or clubs.name like 's%')"),
    ]

    with app.app_context():
        db.session.add_all(conditions)
        db.session.commit()


def create_default_grids(db, app):
    grids = [
        Grid(
            id=5,
            row_condition_1=30,
            row_condition_2=13,
            row_condition_3=16,
            column_condition_1=10,
            column_condition_2=19,
            column_condition_3=41,
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
            row_condition_1=5,
            row_condition_2=23,
            row_condition_3=24,
            column_condition_1=32,
            column_condition_2=29,
            column_condition_3=43,
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
        db.session.add_all(grids)
        db.session.commit()
        db.session.add_all(answers)
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
            name = club_row["Name"]
            country = club_row["Country"]
            league = club_row["League"]
            clubs.append(
                Club(
                    id=club_row["ID"],
                    name=name,
                    country=country,
                    logo=f"https://github.com/Famaral97/clubgrid/blob/main/data/logos/{country}%20-%20{league}/{name}.png?raw=true".replace(
                        " ", "%20"),
                    league=league,
                    has_animal=club_row["Animal"] == "YES",
                    has_winged_animal=club_row["Winged Animal"] == "YES",
                    has_person=club_row["Person"] == "YES",
                    has_football=club_row["Ball"] == "YES",
                    stars_number=club_row["# Stars"],
                    colors_number=club_row["# Colors"],
                    has_numbers=club_row["Numbers"] == "YES",
                    has_color_red=club_row["Red"] == "YES",
                    has_color_blue=club_row["Blue"] == "YES",
                    has_color_green=club_row["Green"] == "YES",
                    league_titles=club_row["League Titles (2024)"],
                    has_crown=club_row["Has Crown"] == "YES",
                    champions_league_titles=club_row["Champions League Titles"],
                    champions_league_runner_up=club_row["Champions League Runner-Up"],
                    europa_league_titles=club_row["Europa League Titles"],
                    europa_league_runner_up=club_row["Europa League Runner-Up"],
                    in_capital=club_row["In Capital City"] == "YES",
                )
            )

    return clubs


def create_default_clubs(db, app):
    clubs = load_clubs()

    with app.app_context():
        db.session.add_all(clubs)
        db.session.commit()
