from dotenv import load_dotenv
import os
import requests

load_dotenv()


while True:
    try:
        response = requests.post(f'{os.getenv("DOMAIN_URL")}{os.getenv("GRID_GENERATION_ENDPOINT")}', timeout=60)

        if response.status_code == 200:
            print("Request succeeded with status code:", response.status_code)
            break
        elif response.status_code == 500:
            print("Request failed with status code:", response.status_code)
        elif response.status_code >= 400:
            print("Request failed with status code:", response.status_code)
            break
        else:
            print("Received status code:", response.status_code)
            break

    except requests.exceptions.Timeout:
        print("The request timed out.")
    except requests.exceptions.RequestException as e:
        # For other errors, print the exception
        print("An error occurred:", e)