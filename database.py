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


def create_default_clubs(db, app):
    clubs = [
        Club(
            id=1,
            name="Alverca",
            logo="https://github.com/luukhopman/football-logos/blob/master/logos/Portugal%20-%20Liga%20Portugal/FC%20Arouca.png?raw=true",
            league="Primeira Liga",
            has_animal=False,
            has_winged_animal=False,
            has_person=False,
            has_football=False,
            stars_number=2,
            colors_number=2,
            has_numbers=False,
            has_color_red=True,
            has_color_blue=False
        ),
        Club(
            id=2,
            name="Benfica",
            logo="https://github.com/luukhopman/football-logos/blob/master/logos/Portugal%20-%20Liga%20Portugal/SL%20Benfica.png?raw=true",
            league="Primeira Liga",
            has_animal=False,
            has_winged_animal=True,
            has_person=False,
            has_football=False,
            stars_number=2,
            colors_number=2,
            has_numbers=False,
            has_color_red=False,
            has_color_blue=False
            )
    ]
    with app.app_context():
        db.session.add_all(clubs)
        db.session.commit()