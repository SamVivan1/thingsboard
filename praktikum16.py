import requests

SERVER = "thingsboard.cloud"
ACCESS_TOKEN = "v3kmg0oatjo12qnoayyp"


url = f"https://{SERVER}/api/v1/{ACCESS_TOKEN}/telemetry"
headers = {
    "Content-Type": "application/json"
}
data_sensor = {
    "temperature": 45,
    "humidity" : 78
}

response = requests.post(url, headers=headers, json=data_sensor)

print('kirim data done')

