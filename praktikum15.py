import requests
from dotenv import load_dotenv
import os

load_dotenv()

THINGSBOARD_SERVER = os.getenv("THINGSBOARD_SERVER")
DEVICE_ID = os.getenv("DEVICE_ID")
API_KEY = os.getenv("API_KEY")

url = f"https://{THINGSBOARD_SERVER}/api/plugins/telemetry/DEVICE/{DEVICE_ID}/values/timeseries"
headers = {
    "X-Authorization": f"ApiKey {API_KEY}"
}

response = requests.get(url, headers=headers)
data = response.json()

print(data)