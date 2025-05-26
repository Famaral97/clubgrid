import csv

from src.models.club import Club


def load_clubs():
    def _to_bool(value):
        return value.strip().upper() == "YES"

    def _build_url(country, name):
        base_url = "https://github.com/Famaral97/clubgrid/blob/main/data/logos"
        return f"{base_url}/{country}/{name}.png?raw=true".replace(" ", "%20")

    with open('./data/data.csv') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',')

        all_clubs = [
            Club(
                id=club_row["id"],
                name=club_row['name'],
                logo=_build_url(country=club_row['country'], name=club_row["name"]),
                country=club_row['country'],

                name_has_number=_to_bool(club_row['name_has_number']),
                logo_has_animal=_to_bool(club_row['logo_has_animal']),
                logo_has_winged_animal=_to_bool(club_row['logo_has_winged_animal']),
                logo_has_person=_to_bool(club_row['logo_has_person']),
                logo_has_football=_to_bool(club_row['logo_has_football']),
                logo_is_circular=_to_bool(club_row['logo_is_circular']),
                logo_has_crown=_to_bool(club_row['logo_has_crown']),
                logo_has_numbers=_to_bool(club_row['logo_has_numbers']),
                num_stars_in_logo=club_row['num_stars_in_logo'],

                num_colors_in_logo=club_row['num_colors_in_logo'],
                logo_has_red=_to_bool(club_row['logo_has_red']),
                logo_has_blue=_to_bool(club_row['logo_has_blue']),
                logo_has_green=_to_bool(club_row['logo_has_green']),
                logo_has_black=_to_bool(club_row['logo_has_black']),

                in_capital=_to_bool(club_row['in_capital']),

                league_titles=club_row['league_titles'],
                tier_2024_25=club_row['tier_2024_25'],
                tier_2023_24=club_row['tier_2023_24'],
                tier_2022_23=club_row['tier_2022_23'],

                domestic_cup_titles=club_row['domestic_cup_titles'],
                domestic_cup_runner_up=club_row['domestic_cup_runner_up'],

                domestic_supercup_titles=club_row['domestic_supercup_titles'],
                domestic_supercup_runner_up=club_row['domestic_supercup_runner_up'],

                champions_league_2024_25=_to_bool(club_row['champions_league_2024_25']),
                champions_league_titles=club_row['champions_league_titles'],
                champions_league_runner_up=club_row['champions_league_runner_up'],

                europa_league_2024_25=_to_bool(club_row['europa_league_2024_25']),
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
            for club_row in csvreader
        ]

    return all_clubs
