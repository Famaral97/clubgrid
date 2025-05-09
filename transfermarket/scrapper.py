import re
from time import sleep
import pandas as pd
import requests
from bs4 import BeautifulSoup


def strip_monetary_value(content):
    if content == "-" or content.lower().startswith("loan"):
        return 0

    if content == "free transfer":
        return 0

    match = re.search(r'€([0-9,.]+)(bn|m|k)', content)
    if match:
        value = float(match.group(1).replace(',', ''))
        if match.group(2) == 'bn':
            return value * 1000
        elif match.group(2) == 'm':
            return value
        elif match.group(2) == 'k':
            return value / 1000
        else:
            Exception("failed to get units")

    print("FAIL")
    print(content)
    Exception("failed to get monetary value")


def get_club_data(club_id):
    url = f"https://www.transfermarkt.com/irrelevant/startseite/verein/{club_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

    tries = 0

    while tries < 3:
        try:
            tries += 1
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            club_data = {
                'tfmk_id': club_id,
                'legal_name': soup.find('span', itemprop="legalName").text.strip(),
                'foundation_year': int(soup.find('span', itemprop="foundingDate").text.strip()[-4:]),
                'most_valuable_player': -1,
                'oldest_player': -1,
                'most_expensive_entry': -1,
                'most_expensive_exit': -1,
            }
            break
        except AttributeError:
            print(f" retry #{tries} ", end="")
            sleep(30)

    # club details on top
    data_header_items = soup.find_all('ul', class_='data-header__items')
    left_items = data_header_items[0].find_all('li')

    for li in left_items:
        label = li.contents[0].strip()
        content = li.find('span', class_='data-header__content').text.strip()
        if label == 'Squad size:':
            club_data['squad_size'] = int(content)
        elif label == 'Average age:':
            club_data['average_age'] = float(content)
        elif label == 'Foreigners:':
            foreigners_count = li.find('a').text.strip()
            foreigners_percentage = (li.find('span', class_='tabellenplatz').text.strip()
                                     .replace(' ', '').replace('%', ''))
            club_data['foreigners_count'] = int(foreigners_count)
            club_data['foreigners_percentage'] = float(foreigners_percentage)

    right_items = data_header_items[1].find_all('li')

    for li in right_items:
        label = li.contents[0].strip()
        content = li.find('span', class_='data-header__content').text.strip()
        if label == 'National team players:':
            club_data['national_team_players'] = int(content)
        elif label == 'Stadium:':
            pattern = r'(?P<name>[\w\s]+)\s+(?P<capacity>[\d\.]+)\s+Seats'
            match = re.match(pattern, content)
            if match:
                club_data['stadium_name'] = match.group('name').strip()
                club_data['stadium_capacity'] = match.group('capacity').replace('.', '').strip()

    # club total value
    data_market_value = soup.find('a', class_='data-header__market-value-wrapper').text.strip()

    club_data['total_market_value'] = strip_monetary_value(data_market_value)

    # players table
    players_table_entry = soup.find('table', class_='items').find_all('tr', {'class': ['odd', 'even']})

    for player in players_table_entry:
        player_value = player.find_all('td')[-1].text.strip()
        value = strip_monetary_value(player_value)
        if club_data['most_valuable_player'] < value:
            club_data['most_valuable_player'] = value

        player_age = player.find_all('td')[5].text.strip()
        pattern = r'\((\d+)\)'
        match = re.search(pattern, player_age)
        if match:
            value = int(match.group(1))
            if club_data['oldest_player'] < value:
                club_data['oldest_player'] = value

    # in/out transfer values
    subcategories = soup.find_all('div', class_='sub-kategorie')

    for subcategory in subcategories:
        if subcategory.text.strip() == 'Top arrivals':
            subcategory_entries = subcategory.parent.find_all('td', class_='rechts')
            for subcategory_entry in subcategory_entries:
                value = strip_monetary_value(subcategory_entry.text.strip())
                if club_data['most_expensive_entry'] < value:
                    club_data['most_expensive_entry'] = value
        elif subcategory.text.strip() == 'Top departures':
            subcategory_entries = subcategory.parent.find_all('td', class_='rechts')
            for subcategory_entry in subcategory_entries:
                value = strip_monetary_value(subcategory_entry.text.strip())
                if club_data['most_expensive_exit'] < value:
                    club_data['most_expensive_exit'] = value

    return club_data


def scrape(data_frame, output_file):
    all_clubs_data = []
    failed_clubs = []
    club_number = 1

    for _, club_row in data_frame.iterrows():
        tfmkt_id = club_row['tfmk_id']
        name = club_row['name']

        print(f"\r🔍{name} [ID {tfmkt_id}] ({club_number})", end="")
        try:
            all_clubs_data.append(get_club_data(tfmkt_id))
            print(f"\r✅{name} [ID {tfmkt_id}] ({club_number})")
        except Exception as error:
            print(f"\r‼️{name} [ID {tfmkt_id}] ({club_number}) -> {error}")
            failed_clubs.append({'tfmk_id': tfmkt_id, 'name': name})

        club_number += 1

    failed_clubs_df = pd.DataFrame(failed_clubs)
    failed_clubs_df.to_csv('failed_clubs.csv', index=False)

    clubs_data_df = pd.DataFrame(all_clubs_data)
    clubs_data_df.to_csv(output_file, index=False)


# df = pd.read_csv('ClubGrid Logo Labelling - ALL_DATA.csv')

# england_df = df[df['Country'] == 'England']
# scrape(england_df, 'scrapped_data_EN.csv')
#
# portugal_df = df[df['Country'] == 'Portugal']
# scrape(portugal_df, 'scrapped_data_PT.csv')

# spain_df = df[df['Country'] == 'Spain']
# scrape(spain_df, 'scrapped_data_ES.csv')

# france_df = df[df['Country'] == 'France']
# scrape(france_df, 'scrapped_data_FR.csv')

# italy_df = df[df['Country'] == 'Italy']
# scrape(italy_df, 'scrapped_data_IT.csv')

# germany_df = df[df['Country'] == 'Germany']
# scrape(germany_df, 'scrapped_data_DE.csv')
#
# sleep(120)

failed_df = pd.read_csv('failed_total_value.csv')
scrape(failed_df, 'scrapped_data_failed_total_value.csv')
