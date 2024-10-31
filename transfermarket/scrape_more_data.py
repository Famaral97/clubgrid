import requests
from bs4 import BeautifulSoup


def get_super_cups_number(titles_list):
    for title in titles_list:
        if ('super cup' in title.text.lower() or 'supercup' in title.text.lower()) and 'uefa' not in title.text.lower():
            return int(title.text.split('x')[0])
    return 0


def get_cup_winners_cups_number(titles_list):
    for title in titles_list:
        if 'cup winners cup winner' in title.text.lower():
            return int(title.text.split('x')[0])
    return 0


def scrape_more_data(clubs_data):

    national_super_cups = []
    cup_winners_cups = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    }

    for index, row in clubs_data.iterrows():
        url = row['url'].replace('startseite', 'erfolge')
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # check if the request was successful

            soup = BeautifulSoup(response.text, 'html.parser')

            titles = soup.select('.large-6 h2')

            super_cups = get_super_cups_number(titles)
            national_super_cups.append(super_cups)

            cup_winners_cup_number = get_cup_winners_cups_number(titles)
            cup_winners_cups.append(cup_winners_cup_number)

        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve data for {row['name']}: {e}")
            national_super_cups.append('N/A')
            cup_winners_cups.append('N/A')

    clubs_data['national_supercups'] = national_super_cups
    clubs_data['cups_winners_cups'] = cup_winners_cups
