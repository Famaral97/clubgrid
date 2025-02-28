import requests

url = "https://clubgrid.pythonanywhere.com/health-check"

response = requests.get(url)
if response.status_code == 200:
    print(f"Success! Status code: {response.status_code}")
else:
    raise Exception(f"Request failed with status code: {response.status_code}")
