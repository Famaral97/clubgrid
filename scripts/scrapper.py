import json
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup


def strip_monetary_value(content):
    pattern = r'€(?P<value>[\d\.]+)m'
    match = re.match(pattern, content)
    if match:
        return float(match.group('value').strip())
    else:
        return -1

def get_club_data(club_id):
    url = f"https://www.transfermarkt.com/irrelevant/startseite/verein/{club_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    club_data = {
        'most_valuable_player': -1,
        'oldest_player': -1,
        'most_expensive_entry': 0,
        'most_expensive_exit': 0
    }

    # club details on top

    data_header_items = soup.find_all('ul', class_='data-header__items')
    left_items = data_header_items[0].find_all('li')

    for li in left_items:
        label = li.contents[0].strip()  # Get the text before the <span> element
        content = li.find('span', class_='data-header__content').text.strip()
        if label == 'Squad size:':
            club_data['squad_size'] = int(content)
        elif label == 'Average age:':
            club_data['average_age'] = float(content)
        elif label == 'Foreigners:':
            foreigners_count = li.find('a').text.strip()
            foreigners_percentage = li.find('span', class_='tabellenplatz').text.strip().replace(' ', '').replace('%', '')
            club_data['foreigners_count'] = int(foreigners_count)
            club_data['foreigners_percentage'] = float(foreigners_percentage)

    right_items = data_header_items[1].find_all('li')

    for li in right_items:
        label = li.contents[0].strip()  # Get the text before the <span> element
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

    # club info
    club_data['legal_name'] = soup.find('span', itemprop="legalName").text.strip()
    club_data['name'] = soup.find('h1', class_='data-header__headline-wrapper').text.strip()
    club_data['founding_date'] = soup.find('span', itemprop="foundingDate").text.strip()

    print(json.dumps(club_data, sort_keys=True, indent=4))

    return club_data


all_clubs_data = []
# for club_id in data_df['Tfmk ID']:
club_data = get_club_data(5)
all_clubs_data.append(club_data)
# continue

clubs_data_df = pd.DataFrame(all_clubs_data)

clubs_data_df.to_csv('clubs_data.csv', index=False)