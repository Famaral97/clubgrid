import csv
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
        'id': club_id,
        'legal_name': soup.find('span', itemprop="legalName").text.strip(),
        'name': soup.find('h1', class_='data-header__headline-wrapper').text.strip(),
        'founding_date': soup.find('span', itemprop="foundingDate").text.strip(),
        'most_valuable_player': -1,
        'oldest_player': -1,
        'most_expensive_entry': -1,
        'most_expensive_exit': -1,
    }

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


all_clubs_data = []

# with open('./ClubGrid_test.csv') as csvfile:
with open('./ClubGrid Logo Labelling - ALL_DATA.csv') as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter=',')

    for club_row in csvreader:
        tfmkt_id = club_row['Tfmk ID']
        short_name = club_row['short_name']

        print(f"\r🔍{short_name} [ID {tfmkt_id}]", end="")
        try:
            all_clubs_data.append(get_club_data(tfmkt_id))
            print(f"\r✅{short_name} [ID {tfmkt_id}]")
        except Exception as error:
            print(f"\r‼️{short_name} [ID {tfmkt_id}] -> {error}")

clubs_data_df = pd.DataFrame(all_clubs_data)
clubs_data_df.to_csv('scrapped_data.csv', index=False)

cg_data = pd.read_csv('ClubGrid Logo Labelling - ALL_DATA.csv')
tfmkt_data = pd.read_csv('scrapped_data.csv')

merged_data = pd.merge(cg_data, tfmkt_data, left_on='Tfmk ID', right_on='id', how='inner')

merged_data.to_csv('../data/data.csv', index=False, encoding='utf-8')

print("Data merged successfully and saved ./merged_data.csv")
