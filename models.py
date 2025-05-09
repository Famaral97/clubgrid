from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint

db = SQLAlchemy()


class Condition(db.Model):
    __tablename__ = 'conditions'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    expression = db.Column(db.String(255))
    tags = db.Column(db.String(255))
    deprecated = db.Column(db.Boolean)


class GridType(db.Model):
    __tablename__ = 'grid_types'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    expression = db.Column(db.String(255))
    exclude_country_conditions = db.Column(db.Boolean)


class Club(db.Model):
    __tablename__ = 'clubs'
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    logo = db.Column(db.String(255))
    country = db.Column(db.String(255))

    name_has_number = db.Column(db.Boolean)
    logo_has_animal = db.Column(db.Boolean)
    logo_has_winged_animal = db.Column(db.Boolean)
    logo_has_person = db.Column(db.Boolean)
    logo_has_football = db.Column(db.Boolean)
    logo_is_circular = db.Column(db.Boolean)
    logo_has_crown = db.Column(db.Boolean)
    logo_has_numbers = db.Column(db.Boolean)
    num_stars_in_logo = db.Column(db.Integer)

    num_colors_in_logo = db.Column(db.String(50))
    logo_has_red = db.Column(db.Boolean)
    logo_has_blue = db.Column(db.Boolean)
    logo_has_green = db.Column(db.Boolean)
    logo_has_black = db.Column(db.Boolean)

    in_capital = db.Column(db.Boolean)

    league_titles = db.Column(db.Integer)
    league_2024_25 = db.Column(db.String(255))
    league_2023_24 = db.Column(db.String(255))
    league_2022_23 = db.Column(db.String(255))

    domestic_cup_titles = db.Column(db.Integer)
    domestic_cup_runner_up = db.Column(db.Integer)

    domestic_supercup_titles = db.Column(db.Integer)
    domestic_supercup_runner_up = db.Column(db.Integer)

    champions_league_2024_25 = db.Column(db.Boolean)
    champions_league_titles = db.Column(db.Integer)
    champions_league_runner_up = db.Column(db.Integer)

    europa_league_2024_25 = db.Column(db.Boolean)
    europa_league_titles = db.Column(db.Integer)
    europa_league_runner_up = db.Column(db.Integer)

    cups_winners_cup_titles = db.Column(db.Integer)
    cups_winners_cup_runner_up = db.Column(db.Integer)

    uefa_super_cup_titles = db.Column(db.Integer)
    uefa_super_cup_runner_up = db.Column(db.Integer)

    club_world_cup_titles = db.Column(db.Integer)
    club_world_cup_runner_up = db.Column(db.Integer)

    best_club_awards = db.Column(db.Integer)
    best_club_runner_up = db.Column(db.Integer)
    best_club_third_place = db.Column(db.Integer)

    instagram_followers = db.Column(db.Integer)

    legal_name = db.Column(db.String(255))
    foundation_year = db.Column(db.Integer)

    most_valuable_player = db.Column(db.Float)
    oldest_player = db.Column(db.Integer)
    most_expensive_entry = db.Column(db.Float)
    most_expensive_exit = db.Column(db.Float)
    squad_size = db.Column(db.Integer)
    average_age = db.Column(db.Float)
    foreigners_count = db.Column(db.Integer)
    foreigners_percentage = db.Column(db.Float)
    national_team_players = db.Column(db.Integer)
    stadium_name = db.Column(db.String(255))
    stadium_capacity = db.Column(db.Integer)
    total_market_value = db.Column(db.Float)

    def __eq__(self, other):
        if isinstance(other, Club):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)  # Ensures uniqueness in sets


class Grid(db.Model):
    __tablename__ = 'grids'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    starting_date = db.Column(db.DateTime)
    type_id = db.Column(db.Integer, db.ForeignKey('grid_types.id'))
    local_id = db.Column(db.Integer)
    row_condition_1 = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    row_condition_2 = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    row_condition_3 = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    column_condition_1 = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    column_condition_2 = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    column_condition_3 = db.Column(db.Integer, db.ForeignKey('conditions.id'))


class Answer(db.Model):
    __tablename__ = 'answers'

    grid_id = db.Column(db.Integer, db.ForeignKey('grids.id'), primary_key=True)
    row_condition_id = db.Column(db.Integer, db.ForeignKey('conditions.id'), primary_key=True)
    column_condition_id = db.Column(db.Integer, db.ForeignKey('conditions.id'), primary_key=True)
    club_id = db.Column(db.String(255), db.ForeignKey('clubs.id'), primary_key=True)
    is_solution = db.Column(db.Boolean)
    count = db.Column(db.Integer)
