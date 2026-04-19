import requests

SERVER = "thingsboard.cloud"
DEVICE_ID = "aa12aac0-3636-11f1-9c01-37a7c07792f2"
API_KEY = "tb_jo4CPe1USWzaCf_gzcL3tXe4-SDVYQmGq8DBysrHeqAzRTDojtnf7kzlzCmITsfBGdKjzw1LLXHTkvfkdn4fyg"


url = f"https://{SERVER}/api/plugins/telemetry/DEVICE/{DEVICE_ID}/SHARED_SCOPE"
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
