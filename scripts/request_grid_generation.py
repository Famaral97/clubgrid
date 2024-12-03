from dotenv import load_dotenv
import os
import requests

load_dotenv()

requests.post(f'{os.getenv("DOMAIN_URL")}{os.getenv("GRID_GENERATION_ENDPOINT")}')