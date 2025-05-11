import csv

from src.models.club import Club


def load_clubs():
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

    return all_clubs
