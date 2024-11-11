import requests

url = "https://clubgrid.pythonanywhere.com"

try:
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Success! Status code: {response.status_code}")
    else:
        print(f"Request failed with status code: {response.status_code}")
except requests.RequestException as e:
    print(f"An error occurred: {e}")