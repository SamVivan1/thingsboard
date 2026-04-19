# 📚 API Reference - ThingsBoard Cloud

## Dokumentasi API ThingsBoard REST untuk Project Ini

---

## 1. Authentication

### API Key Authentication
Digunakan untuk server-to-server atau admin operations.

**Header:**
```
X-Authorization: ApiKey <API_KEY>
```

**Contoh:**
```python
headers = {
    "X-Authorization": "ApiKey tb_jo4CPe1USWzaCf_gzcL3tXe4-SDVYQmGq8DBysrHeqAzRTDojtnf7kzlzCmITsfBGdKjzw1LLXHTkvfkdn4fyg"
}
```

### Access Token Authentication
Digunakan untuk device-to-server communication.

**URL Format:**
```
https://thingsboard.cloud/api/v1/{ACCESS_TOKEN}/endpoint
```

**Contoh:**
```
https://thingsboard.cloud/api/v1/v3kmg0oatjo12qnoayyp/telemetry
```

---

## 2. Telemetry API

### 2.1 Upload Telemetry Data

**Method:** `POST`  
**Endpoint:** `/api/v1/{ACCESS_TOKEN}/telemetry`  
**Authentication:** Access Token (in URL)

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "temperature": 25.5,
  "humidity": 60,
  "pressure": 1013.25
}
```

**Response:**
```
Status: 200 OK
```

**Curl Example:**
```bash
curl -X POST \
  https://thingsboard.cloud/api/v1/v3kmg0oatjo12qnoayyp/telemetry \
  -H 'Content-Type: application/json' \
  -d '{
    "temperature": 25.5,
    "humidity": 60
  }'
```

**Python Example:**
```python
import requests

token = "v3kmg0oatjo12qnoayyp"
url = f"https://thingsboard.cloud/api/v1/{token}/telemetry"
headers = {"Content-Type": "application/json"}
data = {"temperature": 25.5, "humidity": 60}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)  # 200 if success
```

**Supported Data Types:**
- Number: `"temperature": 25.5`
- String: `"location": "Room 1"`
- Boolean: `"active": true`
- Array: `"values": [1, 2, 3]`
- Object: `"config": {"key": "value"}`

---

### 2.2 Retrieve Telemetry Data

**Method:** `GET`  
**Endpoint:** `/api/plugins/telemetry/DEVICE/{DEVICE_ID}/values/timeseries`  
**Authentication:** API Key

**Request Headers:**
```
X-Authorization: ApiKey <API_KEY>
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `keys` | string | Comma-separated list of keys (optional) |
| `startTs` | long | Start timestamp in milliseconds |
| `endTs` | long | End timestamp in milliseconds |
| `limit` | int | Maximum number of records (default: 100) |
| `agg` | string | Aggregation function (NONE, MIN, MAX, AVG) |

**Response:**
```json
{
  "temperature": [
    {
      "ts": 1624089600000,
      "value": "25.5"
    }
  ],
  "humidity": [
    {
      "ts": 1624089600000,
      "value": "60"
    }
  ]
}
```

**Curl Example:**
```bash
curl -X GET \
  "https://thingsboard.cloud/api/plugins/telemetry/DEVICE/aa12aac0-3636-11f1-9c01-37a7c07792f2/values/timeseries?keys=temperature,humidity" \
  -H 'X-Authorization: ApiKey tb_jo4CPe1USWzaCf_gzcL3tXe4-SDVYQmGq8DBysrHeqAzRTDojtnf7kzlzCmITsfBGdKjzw1LLXHTkvfkdn4fyg'
```

**Python Example:**
```python
import requests

device_id = "aa12aac0-3636-11f1-9c01-37a7c07792f2"
api_key = "tb_jo4CPe1USWzaCf_gzcL3tXe4-SDVYQmGq8DBysrHeqAzRTDojtnf7kzlzCmITsfBGdKjzw1LLXHTkvfkdn4fyg"
url = f"https://thingsboard.cloud/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries"
headers = {"X-Authorization": f"ApiKey {api_key}"}
params = {
    "keys": "temperature,humidity",
    "limit": 10
}

response = requests.get(url, headers=headers, params=params)
data = response.json()
print(data)
```

---

## 3. Attributes API

### 3.1 Get Attributes

**Method:** `GET`  
**Endpoint:** `/api/plugins/telemetry/DEVICE/{DEVICE_ID}/{SCOPE}`  
**Authentication:** API Key

**SCOPE Options:**
- `SERVER_SCOPE` - Server-side attributes (private)
- `SHARED_SCOPE` - Shared attributes (dapat diakses client)
- `CLIENT_SCOPE` - Client-side attributes

**Response:**
```json
{
  "led_state": {
    "value": false,
    "lastUpdateTs": 1624089600000
  },
  "lcd_message": {
    "value": "hello dunia",
    "lastUpdateTs": 1624089600000
  }
}
```

---

### 3.2 Create/Update Shared Attributes

**Method:** `POST`  
**Endpoint:** `/api/plugins/telemetry/DEVICE/{DEVICE_ID}/SHARED_SCOPE`  
**Authentication:** API Key

**Request Headers:**
```
X-Authorization: ApiKey <API_KEY>
Content-Type: application/json
```

**Request Body:**
```json
{
  "led_state": true,
  "lcd_message": "hello world",
  "brightness": 85
}
```

**Response:**
```
Status: 200 OK
```

**Curl Example:**
```bash
curl -X POST \
  https://thingsboard.cloud/api/plugins/telemetry/DEVICE/aa12aac0-3636-11f1-9c01-37a7c07792f2/SHARED_SCOPE \
  -H 'X-Authorization: ApiKey tb_jo4CPe1USWzaCf_gzcL3tXe4-SDVYQmGq8DBysrHeqAzRTDojtnf7kzlzCmITsfBGdKjzw1LLXHTkvfkdn4fyg' \
  -H 'Content-Type: application/json' \
  -d '{
    "led_state": true,
    "lcd_message": "hello world"
  }'
```

**Python Example:**
```python
import requests

device_id = "aa12aac0-3636-11f1-9c01-37a7c07792f2"
api_key = "tb_jo4CPe1USWzaCf_gzcL3tXe4-SDVYQmGq8DBysrHeqAzRTDojtnf7kzlzCmITsfBGdKjzw1LLXHTkvfkdn4fyg"
url = f"https://thingsboard.cloud/api/plugins/telemetry/DEVICE/{device_id}/SHARED_SCOPE"
headers = {
    "X-Authorization": f"ApiKey {api_key}",
    "Content-Type": "application/json"
}
data = {
    "led_state": True,
    "lcd_message": "hello world",
    "brightness": 85
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)  # 200 if success
```

**Attribute Types:**
- Boolean: `"enabled": true`
- Number: `"brightness": 85`
- String: `"mode": "auto"`
- JSON Object: `"config": {"key": "value"}`

---

## 4. Device API

### 4.1 Get Device Details

**Method:** `GET`  
**Endpoint:** `/api/device/{DEVICE_ID}`  
**Authentication:** API Key

**Response:**
```json
{
  "id": "aa12aac0-3636-11f1-9c01-37a7c07792f2",
  "name": "Sensor Ruang 1",
  "type": "temperature-sensor",
  "label": "Ruangan 1",
  "active": true,
  "createdTime": 1624089600000,
  "tenantId": "xxxxx"
}
```

---

## 5. Error Handling

### HTTP Status Codes

| Status | Meaning | Solution |
|--------|---------|----------|
| `200` | OK - Request successful | Continue |
| `400` | Bad Request - Invalid format | Check JSON format, parameters |
| `401` | Unauthorized - Auth failed | Verify API Key/Token |
| `403` | Forbidden - Access denied | Check permissions |
| `404` | Not Found - Device/ID invalid | Verify Device ID |
| `429` | Rate Limited - Too many requests | Wait before retrying |
| `500` | Server Error | Retry later or contact support |
| `503` | Service Unavailable | Server maintenance |

### Error Response Format

```json
{
  "message": "Required request header \"X-Authorization\" is not found",
  "statusCode": 401
}
```

### Handling Errors in Python

```python
import requests

def send_data_safe(url, headers, data):
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            print("Success!")
        elif response.status_code == 401:
            print("Authentication failed - check your API Key")
        elif response.status_code == 404:
            print("Device not found - check Device ID")
        elif response.status_code == 429:
            print("Rate limited - wait before retrying")
        else:
            print(f"Error {response.status_code}: {response.text}")
            
    except requests.exceptions.Timeout:
        print("Request timeout - server took too long")
    except requests.exceptions.ConnectionError:
        print("Connection error - check internet connection")
    except Exception as e:
        print(f"Unexpected error: {e}")
```

---

## 6. Rate Limiting

**Default Limits:**
- Per minute: 60 requests
- Per hour: 1000 requests

**Best Practices:**
- Add delay between requests: `time.sleep(1)`
- Batch requests when possible
- Use appropriate timeout values
- Implement retry logic with exponential backoff

---

## 7. Timestamp Format

ThingsBoard menggunakan **milliseconds since epoch** (Unix timestamp × 1000).

**Conversion Examples:**

```python
import time
import datetime

# Get current timestamp in milliseconds
current_ts_ms = int(time.time() * 1000)
print(current_ts_ms)  # 1624089600000

# Convert datetime to milliseconds
dt = datetime.datetime(2021, 6, 18, 12, 0, 0)
ts_ms = int(dt.timestamp() * 1000)
print(ts_ms)  # 1624089600000

# Convert milliseconds back to datetime
ts_ms = 1624089600000
dt = datetime.datetime.fromtimestamp(ts_ms / 1000)
print(dt)  # 2021-06-18 12:00:00
```

---

## 8. MQTT Alternative (Advanced)

Jika ingin menggunakan MQTT protocol (lebih efisien untuk IoT):

**Broker:** `mqtt.thingsboard.cloud`  
**Port:** `1883` (non-SSL) or `8883` (SSL)

**Publish Topics:**
- `v1/devices/me/telemetry` - Send telemetry
- `v1/devices/me/attributes` - Send attributes

**Note:** MQTT implementation tidak termasuk dalam project ini.

---

## 9. API Endpoints Summary

| Operasi | Method | Endpoint | Auth |
|---------|--------|----------|------|
| Upload Telemetry | POST | `/api/v1/{TOKEN}/telemetry` | Token |
| Get Telemetry | GET | `/api/plugins/telemetry/DEVICE/{ID}/values/timeseries` | API Key |
| Get Attributes | GET | `/api/plugins/telemetry/DEVICE/{ID}/{SCOPE}` | API Key |
| Update Attributes | POST | `/api/plugins/telemetry/DEVICE/{ID}/SHARED_SCOPE` | API Key |
| Get Device | GET | `/api/device/{ID}` | API Key |

---

## 10. Complete Request/Response Examples

### Example 1: Complete Temperature Data Send

```python
import requests

def send_temperature():
    token = "v3kmg0oatjo12qnoayyp"
    url = f"https://thingsboard.cloud/api/v1/{token}/telemetry"
    headers = {"Content-Type": "application/json"}
    data = {
        "temperature": 23.5,
        "humidity": 65,
        "timestamp": int(time.time() * 1000)
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("✓ Data sent successfully")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)

send_temperature()
```

### Example 2: Complete Device Control

```python
import requests

def control_led(led_state, message):
    device_id = "aa12aac0-3636-11f1-9c01-37a7c07792f2"
    api_key = "tb_jo4CPe1USWzaCf_gzcL3tXe4-SDVYQmGq8DBysrHeqAzRTDojtnf7kzlzCmITsfBGdKjzw1LLXHTkvfkdn4fyg"
    url = f"https://thingsboard.cloud/api/plugins/telemetry/DEVICE/{device_id}/SHARED_SCOPE"
    headers = {
        "X-Authorization": f"ApiKey {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "led_state": led_state,
        "lcd_message": message
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 200

# Usage
if control_led(True, "LED is ON"):
    print("✓ LED control successful")
else:
    print("✗ LED control failed")
```

---

**API Reference v1.0 - April 2026**
