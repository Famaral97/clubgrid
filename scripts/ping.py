import requests

url = "https://clubgrid.pythonanywhere.com/"

response = requests.get(url, timeout=5)
if response.status_code == 200:
    print(f"Success! Status code: {response.status_code}")
else:
    raise Exception(f"Request failed with status code: {response.status_code}")
