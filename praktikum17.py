import os

from dotenv import load_dotenv
import requests

load_dotenv()

THINGSBOARD_SERVER = os.getenv("THINGSBOARD_SERVER")
DEVICE_ID = os.getenv("DEVICE_ID")
API_KEY = os.getenv("API_KEY")

url = f"https://{THINGSBOARD_SERVER}/api/plugins/telemetry/DEVICE/{DEVICE_ID}/SHARED_SCOPE"
headers = {
    "X-Authorization": f"ApiKey {API_KEY}",
    "Content-Type": "application/json"
}

data_attribute = {
    "led_state": False,
    "lcd_message": "hello dunia"
}

response = requests.post(url, headers=headers, json=data_attribute)


print('\nbuat/update done\n')
