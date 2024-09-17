import csv

from models import Condition, Club


def create_default_conditions(db, app):
    conditions = [
        Condition(id=1, description="Has animal", expression=".has_animal == True"),
        Condition(id=2, description="In Premier League", expression=".league == 'Premier League'"),
        Condition(id=3, description="Starts with A", expression=".name.lower().startswith('a')"),
        Condition(id=4, description="Has Red", expression=".has_color_red == True" ),
        Condition(id=5, description="Does not have Blue", expression=".has_color_blue == False"),
        Condition(id=6, description="Does not have stars", expression=".stars_number == 0")
    ]
    with app.app_context():
        db.session.add_all(conditions)
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
                    logo=f"https://github.com/luukhopman/football-logos/blob/master/logos/{country}%20-%20{league}/{name}.png?raw=true".replace(" ", "%20"),
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