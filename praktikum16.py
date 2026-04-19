import requests
from dotenv import load_dotenv
import os

load_dotenv()

THINGSBOARD_SERVER = os.getenv("THINGSBOARD_SERVER")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


url = f"https://{THINGSBOARD_SERVER}/api/v1/{ACCESS_TOKEN}/telemetry"
headers = {
    "Content-Type": "application/json"
}
data_sensor = {
    "temperature": 45,
    "humidity" : 78
}

response = requests.post(url, headers=headers, json=data_sensor)

print('kirim data done')

