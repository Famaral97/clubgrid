from dotenv import load_dotenv
import os
import requests

load_dotenv()

for grid_type_id in range(1, 8):
    while True:
        try:
            response = requests.post(
                url=f'{os.getenv("DOMAIN_URL")}{os.getenv("GRID_GENERATION_ENDPOINT")}?grid_type_id={grid_type_id}',
                timeout=60
            )

            if response.status_code == 200:
                print(f"Request succeeded for grid type {grid_type_id} with status code: {response.status_code}")
                break
            elif (response.status_code == 500) or (response.status_code >= 400):
                print(f"Request failed with status code: {response.status_code}")
                break
            else:
                print(f"Received status code: {response.status_code}")
                break

        except requests.exceptions.Timeout:
            print("The request timed out.")
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
