import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_club_data(club_id):
    url = f"https://www.transfermarkt.com/irrelevant/startseite/verein/{club_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    data_header_items = soup.find('ul', class_='data-header__items')
    li_elements = data_header_items.find_all('li')

    club_data = {}

    for li in li_elements:
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

    print(club_data)

    return club_data


all_clubs_data = []
# for club_id in data_df['Tfmk ID']:
club_data = get_club_data(5)
all_clubs_data.append(club_data)
# continue

clubs_data_df = pd.DataFrame(all_clubs_data)

clubs_data_df.to_csv('clubs_data.csv', index=False)

print("Data collection complete. The data has been saved to 'clubs_data.csv'.")
