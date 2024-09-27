import csv

from models import Condition, Club, Grid


def create_default_conditions(db, app):
    conditions = [
        Condition(id=1, description="Logo has animal", expression="club.has_animal == True"),
        Condition(id=2, description="In Premier League", expression="club.league == 'Premier League'"),
        Condition(id=3, description="Logo has only 2 colors", expression="club.colors_number == '2'"),
        Condition(id=4, description="Logo has Red", expression="club.has_color_red == True" ),
        Condition(id=5, description="Logo doesn't have Blue", expression="club.has_color_blue == False"),
        Condition(id=6, description="Name starts with A, B or C",
                  expression="club.name.lower().startswith('a') or club.name.lower().startswith('b') or club.name.lower().startswith('c')"),
        Condition(id=7, description="Logo doesn't have stars", expression="club.stars_number == 0")
    ]
    with app.app_context():
        db.session.add_all(conditions)
        db.session.commit()


def create_default_grids(db, app):
    grids = [
        Grid(
            id=2,
            row_condition_1=1,
            row_condition_2=2,
            row_condition_3=3,
            column_condition_1=4,
            column_condition_2=7,
            column_condition_3=6,
        ),
        Grid(
            id=1,
            row_condition_1=4,
            row_condition_2=3,
            row_condition_3=5,
            column_condition_1=7,
            column_condition_2=1,
            column_condition_3=2,
        )
    ]
    with app.app_context():
        db.session.add_all(grids)
        db.session.commit()


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
                    logo=f"https://github.com/Famaral97/clubgrid/blob/main/data/logos/{country}%20-%20{league}/{name}.png?raw=true".replace(" ", "%20"),
                    league=league,
                    has_animal=club_row["Animal"]=="YES",
                    has_winged_animal=club_row["Winged Animal"]=="YES",
                    has_person=club_row["Person"]=="YES",
                    has_football=club_row["Ball"]=="YES",
                    stars_number=club_row["# Stars"],
                    colors_number=club_row["# Colors"],
                    has_numbers=club_row["Numbers"]=="YES",
                    has_color_red=club_row["Red"]=="YES",
                    has_color_blue=club_row["Blue"]=="YES"
                )
            )

    return clubs


def create_default_clubs(db, app):
    clubs = load_clubs()

    with app.app_context():
        db.session.add_all(clubs)
        db.session.commit()