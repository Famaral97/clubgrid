import os

import pandas as pd
import requests


def get_logo(name, tfmkt_id, league_id):
    url = f"https://tmssl.akamaized.net//images/wappen/head/{tfmkt_id}.png"
    folder_path = f"../data/logos/{league_id}"
    response = requests.get(url)

    if response.status_code == 200:
        image_path = os.path.join(folder_path, f"{name}.png")

        with open(image_path, 'wb') as file:
            file.write(response.content)

    else:
        Exception("Failed to download image")


def scrape_logos(df, league_id):
    df = df[df['league_2024_25'] == league_id]

    club_number = 1

    for _, club_row in df.iterrows():
        tfmkt_id = club_row['tfmk_id']
        name = club_row['name']

        print(f"\r🔍{name} [ID {tfmkt_id}] ({club_number})", end="")
        try:
            get_logo(name, tfmkt_id, league_id)
            print(f"\r✅{name} [ID {tfmkt_id}] ({club_number})")
        except Exception as error:
            print(f"\r‼️{name} [ID {tfmkt_id}] ({club_number}) -> {error}")

        club_number += 1


scrape_logos(
    df=pd.read_csv('ClubGrid Logo Labelling - ALL_DATA.csv'),
    league_id='EN2'
)
