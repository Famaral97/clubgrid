import csv
from datetime import datetime, timedelta

from sqlalchemy import text, inspect, desc
from sqlalchemy.dialects.mysql import insert

from models import Condition, Club, Grid, Answer, MetaCondition


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


def create_default_meta_conditions(db, app):
    meta_conditions = [
        MetaCondition(id=1, description='Big 6',
                      expression="clubs.country in ('Italy', 'Portugal', 'England', 'Spain', 'France', 'Germany')"
                      ),
        MetaCondition(id=2, description='Portugal',
                      expression="clubs.country = 'Portugal'",
                      exclude_country_conditions=True
                      ),
        # MetaCondition(id=3, description='Germany', expression="clubs.country = 'Germany'"),
        # MetaCondition(id=4, description='England', expression="clubs.country = 'England'"),
        # MetaCondition(id=5, description='Italy', expression="clubs.country = 'Italy'"),
        # MetaCondition(id=6, description='Spain', expression="clubs.country = 'Spain'"),
        # MetaCondition(id=7, description='France', expression="clubs.country = 'France'"),
    ]

    with app.app_context():
        stmt = insert(MetaCondition).values([to_dict(meta_condition) for meta_condition in meta_conditions])
        stmt = stmt.on_duplicate_key_update(stmt.inserted)
        db.session.execute(stmt)
        db.session.commit()


def create_default_grids(db, app):
    grids = [
        Grid(
            id=1,
            meta_condition_id=1,
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
            meta_condition_id=2,
            local_id=1,
            starting_date=datetime(2024, 12, 4, 0, 0),
            row_condition_1=54,
            row_condition_2=67,
            row_condition_3=2,
            column_condition_1=60,
            column_condition_2=79,
            column_condition_3=4,
        ),
        # Grid(
        #     id=47,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 12, 3, 0, 0),
        #     row_condition_1=6,
        #     row_condition_2=49,
        #     row_condition_3=69,
        #     column_condition_1=36,
        #     column_condition_2=31,
        #     column_condition_3=76,
        # ),
        # Grid(
        #     id=46,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 12, 2, 0, 0),
        #     row_condition_1=70,
        #     row_condition_2=50,
        #     row_condition_3=1,
        #     column_condition_1=33,
        #     column_condition_2=81,
        #     column_condition_3=53,
        # ),
        # Grid(
        #     id=45,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 12, 1, 0, 0),
        #     row_condition_1=64,
        #     row_condition_2=23,
        #     row_condition_3=12,
        #     column_condition_1=75,
        #     column_condition_2=37,
        #     column_condition_3=86,
        # ),
        # Grid(
        #     id=44,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 30, 0, 0),
        #     row_condition_1=8,
        #     row_condition_2=13,
        #     row_condition_3=78,
        #     column_condition_1=22,
        #     column_condition_2=29,
        #     column_condition_3=97,
        # ),
        # Grid(
        #     id=43,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 29, 0, 0),
        #     row_condition_1=39,
        #     row_condition_2=83,
        #     row_condition_3=51,
        #     column_condition_1=4,
        #     column_condition_2=100,
        #     column_condition_3=98,
        # ),
        # Grid(
        #     id=42,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 28, 0, 0),
        #     row_condition_1=67,
        #     row_condition_2=85,
        #     row_condition_3=15,
        #     column_condition_1=26,
        #     column_condition_2=55,
        #     column_condition_3=7,
        # ),
        # Grid(
        #     id=41,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 27, 0, 0),
        #     row_condition_1=48,
        #     row_condition_2=38,
        #     row_condition_3=19,
        #     column_condition_1=3,
        #     column_condition_2=43,
        #     column_condition_3=59,
        # ),
        # Grid(
        #     id=40,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 26, 0, 0),
        #     row_condition_1=96,
        #     row_condition_2=2,
        #     row_condition_3=46,
        #     column_condition_1=17,
        #     column_condition_2=5,
        #     column_condition_3=69,
        # ),
        # Grid(
        #     id=39,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 25, 0, 0),
        #     row_condition_1=8,
        #     row_condition_2=74,
        #     row_condition_3=47,
        #     column_condition_1=102,
        #     column_condition_2=56,
        #     column_condition_3=71,
        # ),
        # Grid(
        #     id=38,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 24, 0, 0),
        #     row_condition_1=83,
        #     row_condition_2=22,
        #     row_condition_3=34,
        #     column_condition_1=9,
        #     column_condition_2=6,
        #     column_condition_3=98,
        # ),
        # Grid(
        #     id=37,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 23, 0, 0),
        #     row_condition_1=23,
        #     row_condition_2=88,
        #     row_condition_3=44,
        #     column_condition_1=68,
        #     column_condition_2=81,
        #     column_condition_3=42,
        # ),
        # Grid(
        #     id=36,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 22, 0, 0),
        #     row_condition_1=51,
        #     row_condition_2=62,
        #     row_condition_3=21,
        #     column_condition_1=69,
        #     column_condition_2=100,
        #     column_condition_3=33,
        # ),
        # Grid(
        #     id=35,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 21, 0, 0),
        #     row_condition_1=3,
        #     row_condition_2=76,
        #     row_condition_3=72,
        #     column_condition_1=28,
        #     column_condition_2=93,
        #     column_condition_3=31,
        # ),
        # Grid(
        #     id=34,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 20, 0, 0),
        #     row_condition_1=7,
        #     row_condition_2=30,
        #     row_condition_3=60,
        #     column_condition_1=45,
        #     column_condition_2=65,
        #     column_condition_3=35,
        # ),
        # Grid(
        #     id=33,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 19, 0, 0),
        #     row_condition_1=2,
        #     row_condition_2=92,
        #     row_condition_3=97,
        #     column_condition_1=70,
        #     column_condition_2=66,
        #     column_condition_3=103,
        # ),
        # Grid(
        #     id=32,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 18, 0, 0),
        #     row_condition_1=102,
        #     row_condition_2=75,
        #     row_condition_3=94,
        #     column_condition_1=86,
        #     column_condition_2=24,
        #     column_condition_3=73,
        # ),
        # Grid(
        #     id=31,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 17, 0, 0),
        #     row_condition_1=4,
        #     row_condition_2=55,
        #     row_condition_3=84,
        #     column_condition_1=21,
        #     column_condition_2=90,
        #     column_condition_3=25,
        # ),
        # Grid(
        #     id=30,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 16, 0, 0),
        #     row_condition_1=82,
        #     row_condition_2=96,
        #     row_condition_3=50,
        #     column_condition_1=76,
        #     column_condition_2=62,
        #     column_condition_3=3,
        # ),
        # Grid(
        #     id=29,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 15, 0, 0),
        #     row_condition_1=7,
        #     row_condition_2=18,
        #     row_condition_3=59,
        #     column_condition_1=20,
        #     column_condition_2=74,
        #     column_condition_3=38,
        # ),
        # Grid(
        #     id=28,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 14, 0, 0),
        #     row_condition_1=78,
        #     row_condition_2=40,
        #     row_condition_3=53,
        #     column_condition_1=2,
        #     column_condition_2=24,
        #     column_condition_3=32,
        # ),
        # Grid(
        #     id=27,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 13, 0, 0),
        #     row_condition_1=4,
        #     row_condition_2=69,
        #     row_condition_3=9,
        #     column_condition_1=19,
        #     column_condition_2=87,
        #     column_condition_3=92,
        # ),
        # Grid(
        #     id=26,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 12, 0, 0),
        #     row_condition_1=88,
        #     row_condition_2=99,
        #     row_condition_3=55,
        #     column_condition_1=83,
        #     column_condition_2=91,
        #     column_condition_3=102,
        # ),
        # Grid(
        #     id=25,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 11, 0, 0),
        #     row_condition_1=6,
        #     row_condition_2=85,
        #     row_condition_3=44,
        #     column_condition_1=67,
        #     column_condition_2=23,
        #     column_condition_3=57,
        # ),
        # Grid(
        #     id=24,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 10, 0, 0),
        #     row_condition_1=100,
        #     row_condition_2=66,
        #     row_condition_3=11,
        #     column_condition_1=25,
        #     column_condition_2=97,
        #     column_condition_3=41,
        # ),
        # Grid(
        #     id=23,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 9, 0, 0),
        #     row_condition_1=72,
        #     row_condition_2=91,
        #     row_condition_3=58,
        #     column_condition_1=22,
        #     column_condition_2=10,
        #     column_condition_3=36,
        # ),
        # Grid(
        #     id=22,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 8, 0, 0),
        #     row_condition_1=35,
        #     row_condition_2=8,
        #     row_condition_3=67,
        #     column_condition_1=20,
        #     column_condition_2=92,
        #     column_condition_3=74,
        # ),
        # Grid(
        #     id=21,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 7, 0, 0),
        #     row_condition_1=3,
        #     row_condition_2=12,
        #     row_condition_3=37,
        #     column_condition_1=53,
        #     column_condition_2=65,
        #     column_condition_3=73,
        # ),
        # Grid(
        #     id=20,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 6, 0, 0),
        #     row_condition_1=38,
        #     row_condition_2=79,
        #     row_condition_3=14,
        #     column_condition_1=40,
        #     column_condition_2=54,
        #     column_condition_3=68,
        # ),
        # Grid(
        #     id=19,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 5, 0, 0),
        #     row_condition_1=41,
        #     row_condition_2=77,
        #     row_condition_3=51,
        #     column_condition_1=75,
        #     column_condition_2=63,
        #     column_condition_3=42,
        # ),
        # Grid(
        #     id=18,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 4, 0, 0),
        #     row_condition_1=62,
        #     row_condition_2=21,
        #     row_condition_3=83,
        #     column_condition_1=8,
        #     column_condition_2=71,
        #     column_condition_3=66,
        # ),
        # Grid(
        #     id=17,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 3, 0, 0),
        #     row_condition_1=24,
        #     row_condition_2=32,
        #     row_condition_3=65,
        #     column_condition_1=72,
        #     column_condition_2=76,
        #     column_condition_3=61,
        # ),
        # Grid(
        #     id=16,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 2, 0, 0),
        #     row_condition_1=21,
        #     row_condition_2=68,
        #     row_condition_3=79,
        #     column_condition_1=64,
        #     column_condition_2=74,
        #     column_condition_3=53,
        # ),
        # Grid(
        #     id=15,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 11, 1, 0, 0),
        #     row_condition_1=50,
        #     row_condition_2=47,
        #     row_condition_3=41,
        #     column_condition_1=60,
        #     column_condition_2=75,
        #     column_condition_3=43,
        # ),
        # Grid(
        #     id=14,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 10, 31, 0, 0),
        #     row_condition_1=65,
        #     row_condition_2=40,
        #     row_condition_3=39,
        #     column_condition_1=27,
        #     column_condition_2=42,
        #     column_condition_3=58,
        # ),
        # Grid(
        #     id=13,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 10, 30, 0, 0),
        #     row_condition_1=73,
        #     row_condition_2=68,
        #     row_condition_3=28,
        #     column_condition_1=75,
        #     column_condition_2=12,
        #     column_condition_3=54,
        # ),
        # Grid(
        #     id=12,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 10, 29, 0, 0),
        #     row_condition_1=67,
        #     row_condition_2=14,
        #     row_condition_3=69,
        #     column_condition_1=55,
        #     column_condition_2=17,
        #     column_condition_3=75,
        # ),
        # Grid(
        #     id=11,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 10, 28, 0, 0),
        #     row_condition_1=50,
        #     row_condition_2=8,
        #     row_condition_3=54,
        #     column_condition_1=34,
        #     column_condition_2=15,
        #     column_condition_3=74,
        # ),
        # Grid(
        #     id=10,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 10, 27, 0, 0),
        #     row_condition_1=24,
        #     row_condition_2=5,
        #     row_condition_3=73,
        #     column_condition_1=52,
        #     column_condition_2=11,
        #     column_condition_3=10,
        # ),
        # Grid(
        #     id=9,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 10, 26, 0, 0),
        #     row_condition_1=74,
        #     row_condition_2=17,
        #     row_condition_3=50,
        #     column_condition_1=71,
        #     column_condition_2=48,
        #     column_condition_3=28,
        # ),
        # Grid(
        #     id=8,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 10, 25, 0, 0),
        #     row_condition_1=70,
        #     row_condition_2=19,
        #     row_condition_3=6,
        #     column_condition_1=79,
        #     column_condition_2=48,
        #     column_condition_3=31,
        # ),
        # Grid(
        #     id=7,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 10, 24, 0, 0),
        #     row_condition_1=32,
        #     row_condition_2=52,
        #     row_condition_3=26,
        #     column_condition_1=49,
        #     column_condition_2=2,
        #     column_condition_3=41,
        # ),
        # Grid(
        #     id=6,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 10, 23, 0, 0),
        #     row_condition_1=30,
        #     row_condition_2=41,
        #     row_condition_3=27,
        #     column_condition_1=54,
        #     column_condition_2=21,
        #     column_condition_3=50,
        # ),
        # Grid(
        #     id=5,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 10, 22, 0, 0),
        #     row_condition_1=36,
        #     row_condition_2=1,
        #     row_condition_3=10,
        #     column_condition_1=62,
        #     column_condition_2=67,
        #     column_condition_3=73,
        # ),
        # Grid(
        #     id=4,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 10, 21, 0, 0),
        #     row_condition_1=63,
        #     row_condition_2=77,
        #     row_condition_3=78,
        #     column_condition_1=52,
        #     column_condition_2=4,
        #     column_condition_3=29,
        # ),
        # Grid(
        #     id=3,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 10, 20, 0, 0),
        #     row_condition_1=32,
        #     row_condition_2=22,
        #     row_condition_3=7,
        #     column_condition_1=15,
        #     column_condition_2=25,
        #     column_condition_3=9,
        # ),
        # Grid(
        #     id=2,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 10, 19, 0, 0),
        #     row_condition_1=1,
        #     row_condition_2=3,
        #     row_condition_3=17,
        #     column_condition_1=20,
        #     column_condition_2=28,
        #     column_condition_3=42,
        # ),
        # Grid(
        #     id=1,
        #     meta_condition_id=1,
        #     starting_date=datetime(2024, 10, 18, 0, 0),
        #     row_condition_1=30,
        #     row_condition_2=13,
        #     row_condition_3=16,
        #     column_condition_1=10,
        #     column_condition_2=19,
        #     column_condition_3=41,
        # ),
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
        meta_condition = MetaCondition.query.get(
            grid.meta_condition_id) if grid.meta_condition_id else MetaCondition.query.get(1)

    grid_answers = []
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_1, grid.row_condition_1, meta_condition, app))
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_1, grid.row_condition_2, meta_condition, app))
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_1, grid.row_condition_3, meta_condition, app))
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_2, grid.row_condition_1, meta_condition, app))
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_2, grid.row_condition_2, meta_condition, app))
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_2, grid.row_condition_3, meta_condition, app))
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_3, grid.row_condition_1, meta_condition, app))
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_3, grid.row_condition_2, meta_condition, app))
    grid_answers.extend(get_cell_answers(grid, grid.column_condition_3, grid.row_condition_3, meta_condition, app))
    return grid_answers


def get_cell_answers(grid, column_condition_id, row_condition_id, meta_condition, app):
    with app.app_context():
        query = Club.query.filter(
            text(Condition.query.get(row_condition_id).expression),
            text(Condition.query.get(column_condition_id).expression)
        )

        if meta_condition is not None:
            query = query.filter(text(meta_condition.expression))

        solution_clubs = query.all()

    return [Answer(
        grid_id=grid.id,
        column_condition_id=column_condition_id,
        row_condition_id=row_condition_id,
        club_id=club.id,
        is_solution=True,
        count=0,
    ) for club in solution_clubs]


def get_grid_solution(row_conditions, column_conditions, meta_condition, app):
    return [
        [
            get_cell_solution(row_conditions[0], column_conditions[0], meta_condition, app),
            get_cell_solution(row_conditions[0], column_conditions[1], meta_condition, app),
            get_cell_solution(row_conditions[0], column_conditions[2], meta_condition, app)
        ],
        [
            get_cell_solution(row_conditions[1], column_conditions[0], meta_condition, app),
            get_cell_solution(row_conditions[1], column_conditions[1], meta_condition, app),
            get_cell_solution(row_conditions[1], column_conditions[2], meta_condition, app)
        ],
        [
            get_cell_solution(row_conditions[2], column_conditions[0], meta_condition, app),
            get_cell_solution(row_conditions[2], column_conditions[1], meta_condition, app),
            get_cell_solution(row_conditions[2], column_conditions[2], meta_condition, app)
        ]
    ]


def get_cell_solution(row_condition, col_condition, grid_meta_condition, app):
    with app.app_context():
        query = Club.query.filter(text(row_condition.expression), text(col_condition.expression))

        if grid_meta_condition is not None:
            query = query.filter(text(grid_meta_condition.expression))

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


def insert_grid(db, app, row_conditions, column_conditions, grid_meta_condition):
    newest_local_grid = Grid.query.filter(Grid.meta_condition_id == grid_meta_condition.id).order_by(desc(Grid.local_id)).first()
    grid_local_id = (newest_local_grid.local_id if newest_local_grid else 0) + 1

    new_grid_date = Grid.query.order_by(desc(Grid.id)).first().starting_date + timedelta(days=1)

    new_grid = Grid(
        local_id=grid_local_id,
        meta_condition_id=grid_meta_condition.id,
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
