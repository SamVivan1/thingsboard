import requests

SERVER = "thingsboard.cloud"
DEVICE_ID = "aa12aac0-3636-11f1-9c01-37a7c07792f2"
API_KEY = "tb_jo4CPe1USWzaCf_gzcL3tXe4-SDVYQmGq8DBysrHeqAzRTDojtnf7kzlzCmITsfBGdKjzw1LLXHTkvfkdn4fyg"

url = f"https://{SERVER}/api/plugins/telemetry/DEVICE/{DEVICE_ID}/values/timeseries"
headers = {
    "X-Authorization": f"ApiKey {API_KEY}"
}

response = requests.get(url, headers=headers)
data = response.json()

print(data)