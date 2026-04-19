# 🔧 Advanced Usage & Examples - ThingsBoard

## Contoh-Contoh Penggunaan Lanjutan dan Use Cases Praktis

---

## 1. Enhanced Praktikum 16 - Mengirim Data Sensor dengan Error Handling

### Versi Dasar
```python
import requests
import time

SERVER = "thingsboard.cloud"
ACCESS_TOKEN = "v3kmg0oatjo12qnoayyp"

def send_sensor_data(temperature, humidity):
    url = f"https://{SERVER}/api/v1/{ACCESS_TOKEN}/telemetry"
    headers = {"Content-Type": "application/json"}
    data = {
        "temperature": temperature,
        "humidity": humidity,
        "timestamp": int(time.time() * 1000)
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            print(f"✓ Data sent: Temp={temperature}°C, Humidity={humidity}%")
            return True
        else:
            print(f"✗ Error {response.status_code}: {response.text}")
            return False
    except requests.exceptions.Timeout:
        print("✗ Timeout - server tidak merespons")
        return False
    except requests.exceptions.ConnectionError:
        print("✗ Connection error - periksa internet")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

# Penggunaan
send_sensor_data(temperature=25.5, humidity=60)
```

---

### Versi Advanced - Loop dengan Retry

```python
import requests
import time
from datetime import datetime

SERVER = "thingsboard.cloud"
ACCESS_TOKEN = "v3kmg0oatjo12qnoayyp"

class SensorDataSender:
    def __init__(self, access_token, server="thingsboard.cloud"):
        self.token = access_token
        self.server = server
        self.url = f"https://{self.server}/api/v1/{self.token}/telemetry"
        self.headers = {"Content-Type": "application/json"}
        
    def send_data(self, sensor_data, retries=3):
        """
        Kirim data sensor dengan retry logic
        
        Args:
            sensor_data (dict): Data sensor yang akan dikirim
            retries (int): Jumlah percobaan
            
        Returns:
            bool: True jika berhasil, False jika gagal
        """
        for attempt in range(retries):
            try:
                response = requests.post(
                    self.url, 
                    headers=self.headers, 
                    json=sensor_data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Data sent successfully")
                    return True
                    
                elif response.status_code == 429:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"Rate limited. Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                    
                else:
                    print(f"Error {response.status_code}: {response.text}")
                    if attempt < retries - 1:
                        time.sleep(1)
                        
            except Exception as e:
                print(f"Attempt {attempt + 1}/{retries} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(1)
        
        return False
    
    def send_continuous(self, interval_seconds=60):
        """
        Kirim data sensor secara periodik
        
        Args:
            interval_seconds (int): Interval pengiriman dalam detik
        """
        print("Starting continuous data sending... (Press Ctrl+C to stop)")
        try:
            while True:
                # Simulasi pembacaan sensor
                temperature = 20 + (time.time() % 10)  # Random 20-30
                humidity = 50 + (time.time() % 30)     # Random 50-80
                
                sensor_data = {
                    "temperature": round(temperature, 2),
                    "humidity": round(humidity, 2),
                    "timestamp": int(time.time() * 1000)
                }
                
                self.send_data(sensor_data)
                print(f"Next send in {interval_seconds}s...")
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print("\nData sending stopped.")

# Penggunaan
if __name__ == "__main__":
    sender = SensorDataSender(ACCESS_TOKEN)
    
    # Option 1: Send single data
    sensor_data = {
        "temperature": 25.5,
        "humidity": 60,
        "pressure": 1013.25
    }
    sender.send_data(sensor_data)
    
    # Option 2: Send continuous (uncomment untuk dijalankan)
    # sender.send_continuous(interval_seconds=30)
```

---

## 2. Enhanced Praktikum 15 - Membaca Data dengan Visualisasi

### Versi Dasar
```python
import requests
import json

SERVER = "thingsboard.cloud"
DEVICE_ID = "aa12aac0-3636-11f1-9c01-37a7c07792f2"
API_KEY = "tb_jo4CPe1USWzaCf_gzcL3tXe4-SDVYQmGq8DBysrHeqAzRTDojtnf7kzlzCmITsfBGdKjzw1LLXHTkvfkdn4fyg"

def get_sensor_data():
    url = f"https://{SERVER}/api/plugins/telemetry/DEVICE/{DEVICE_ID}/values/timeseries"
    headers = {"X-Authorization": f"ApiKey {API_KEY}"}
    params = {
        "keys": "temperature,humidity,pressure",
        "limit": 10
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Failed to fetch data: {e}")
        return None

# Penggunaan
data = get_sensor_data()
if data:
    print(json.dumps(data, indent=2))
```

### Versi Advanced - Parse & Display

```python
import requests
import json
from datetime import datetime
from collections import defaultdict

SERVER = "thingsboard.cloud"
DEVICE_ID = "aa12aac0-3636-11f1-9c01-37a7c07792f2"
API_KEY = "tb_jo4CPe1USWzaCf_gzcL3tXe4-SDVYQmGq8DBysrHeqAzRTDojtnf7kzlzCmITsfBGdKjzw1LLXHTkvfkdn4fyg"

class SensorDataReader:
    def __init__(self, device_id, api_key, server="thingsboard.cloud"):
        self.device_id = device_id
        self.api_key = api_key
        self.server = server
        self.url = f"https://{self.server}/api/plugins/telemetry/DEVICE/{self.device_id}/values/timeseries"
        self.headers = {"X-Authorization": f"ApiKey {self.api_key}"}
    
    def get_latest_data(self, keys=None, limit=100):
        """
        Ambil data terbaru dari sensor
        
        Args:
            keys (str): Comma-separated keys (e.g., "temperature,humidity")
            limit (int): Jumlah data yang diambil
            
        Returns:
            dict: Data sensor
        """
        params = {}
        if keys:
            params["keys"] = keys
        params["limit"] = limit
        
        try:
            response = requests.get(self.url, headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"Failed to fetch data: {e}")
            return None
    
    def parse_data(self, raw_data):
        """
        Parse raw API data menjadi format yang lebih mudah dibaca
        """
        parsed = {}
        for key, values in raw_data.items():
            parsed[key] = {
                "latest": values[0]["value"] if values else None,
                "timestamp": datetime.fromtimestamp(values[0]["ts"] / 1000) if values else None,
                "history": values
            }
        return parsed
    
    def display_data_table(self, raw_data):
        """
        Tampilkan data dalam format tabel
        """
        print("\n" + "="*60)
        print("SENSOR DATA SUMMARY")
        print("="*60)
        
        for key, values in raw_data.items():
            if values:
                latest = values[0]
                ts = datetime.fromtimestamp(latest["ts"] / 1000)
                value = latest["value"]
                
                print(f"\n{key.upper()}")
                print(f"  Value:     {value}")
                print(f"  Time:      {ts.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"  Records:   {len(values)}")
    
    def get_statistics(self, raw_data):
        """
        Hitung statistik dari data
        """
        stats = {}
        
        for key, values in raw_data.items():
            numeric_values = []
            for v in values:
                try:
                    numeric_values.append(float(v["value"]))
                except ValueError:
                    continue
            
            if numeric_values:
                stats[key] = {
                    "min": min(numeric_values),
                    "max": max(numeric_values),
                    "avg": sum(numeric_values) / len(numeric_values),
                    "count": len(numeric_values)
                }
        
        return stats
    
    def export_csv(self, raw_data, filename="sensor_data.csv"):
        """
        Export data ke CSV file
        """
        import csv
        
        # Flatten data structure untuk CSV
        rows = []
        max_records = max(len(values) for values in raw_data.values())
        
        for i in range(max_records):
            row = {}
            for key, values in raw_data.items():
                if i < len(values):
                    row[f"{key}_value"] = values[i]["value"]
                    row[f"{key}_time"] = datetime.fromtimestamp(values[i]["ts"] / 1000)
            rows.append(row)
        
        if rows:
            with open(filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            print(f"✓ Data exported to {filename}")

# Penggunaan
if __name__ == "__main__":
    reader = SensorDataReader(DEVICE_ID, API_KEY)
    
    # Get data
    data = reader.get_latest_data(keys="temperature,humidity,pressure", limit=100)
    
    if data:
        # Display table
        reader.display_data_table(data)
        
        # Get statistics
        stats = reader.get_statistics(data)
        print("\nSTATISTICS:")
        for key, stat in stats.items():
            print(f"\n{key}:")
            print(f"  Min:  {stat['min']}")
            print(f"  Max:  {stat['max']}")
            print(f"  Avg:  {stat['avg']:.2f}")
            print(f"  Count: {stat['count']}")
        
        # Export to CSV
        reader.export_csv(data)
```

---

## 3. Enhanced Praktikum 17 - Device Control dengan States

### Versi Dasar
```python
import requests

SERVER = "thingsboard.cloud"
DEVICE_ID = "aa12aac0-3636-11f1-9c01-37a7c07792f2"
API_KEY = "tb_jo4CPe1USWzaCf_gzcL3tXe4-SDVYQmGq8DBysrHeqAzRTDojtnf7kzlzCmITsfBGdKjzw1LLXHTkvfkdn4fyg"

def control_device(attributes):
    url = f"https://{SERVER}/api/plugins/telemetry/DEVICE/{DEVICE_ID}/SHARED_SCOPE"
    headers = {
        "X-Authorization": f"ApiKey {API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=attributes)
    print('Update done') if response.status_code == 200 else print(f'Error: {response.status_code}')

# Penggunaan
control_device({
    "led_state": True,
    "lcd_message": "hello dunia"
})
```

### Versi Advanced - State Management

```python
import requests
from datetime import datetime

SERVER = "thingsboard.cloud"
DEVICE_ID = "aa12aac0-3636-11f1-9c01-37a7c07792f2"
API_KEY = "tb_jo4CPe1USWzaCf_gzcL3tXe4-SDVYQmGq8DBysrHeqAzRTDojtnf7kzlzCmITsfBGdKjzw1LLXHTkvfkdn4fyg"

class DeviceController:
    def __init__(self, device_id, api_key, server="thingsboard.cloud"):
        self.device_id = device_id
        self.api_key = api_key
        self.server = server
        self.base_url = f"https://{self.server}/api/plugins/telemetry/DEVICE/{self.device_id}"
        self.headers = {
            "X-Authorization": f"ApiKey {self.api_key}",
            "Content-Type": "application/json"
        }
        self.current_state = {}
    
    def update_attributes(self, attributes):
        """
        Update shared attributes
        
        Args:
            attributes (dict): Attributes yang akan diupdate
            
        Returns:
            bool: True jika berhasil
        """
        url = f"{self.base_url}/SHARED_SCOPE"
        
        try:
            response = requests.post(url, headers=self.headers, json=attributes, timeout=10)
            if response.status_code == 200:
                self.current_state.update(attributes)
                print(f"✓ Attributes updated at {datetime.now().strftime('%H:%M:%S')}")
                print(f"  {attributes}")
                return True
            else:
                print(f"✗ Error {response.status_code}: {response.text}")
                return False
        except Exception as e:
            print(f"✗ Failed to update: {e}")
            return False
    
    def get_attributes(self, scope="SHARED_SCOPE"):
        """
        Baca attributes dari device
        
        Args:
            scope (str): SHARED_SCOPE, SERVER_SCOPE, atau CLIENT_SCOPE
            
        Returns:
            dict: Attributes yang terbaca
        """
        url = f"{self.base_url}/{scope}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error {response.status_code}")
                return None
        except Exception as e:
            print(f"Failed to get attributes: {e}")
            return None
    
    def toggle_led(self):
        """Toggle LED state"""
        new_state = not self.current_state.get("led_state", False)
        return self.update_attributes({"led_state": new_state})
    
    def set_brightness(self, level):
        """
        Set brightness level (0-100)
        
        Args:
            level (int): Brightness level (0-100)
        """
        if 0 <= level <= 100:
            return self.update_attributes({"brightness": level})
        else:
            print("Brightness harus antara 0-100")
            return False
    
    def set_mode(self, mode):
        """
        Set device mode
        
        Args:
            mode (str): Mode (e.g., "auto", "manual", "night")
        """
        return self.update_attributes({"mode": mode})
    
    def display_status(self):
        """Tampilkan status device saat ini"""
        print("\n" + "="*40)
        print("DEVICE STATUS")
        print("="*40)
        
        attrs = self.get_attributes()
        if attrs:
            for key, attr_data in attrs.items():
                value = attr_data.get("value", "N/A")
                timestamp = attr_data.get("lastUpdateTs", "N/A")
                dt = datetime.fromtimestamp(timestamp / 1000) if timestamp != "N/A" else "N/A"
                
                print(f"\n{key}:")
                print(f"  Value:     {value}")
                print(f"  Updated:   {dt}")

# Penggunaan
if __name__ == "__main__":
    controller = DeviceController(DEVICE_ID, API_KEY)
    
    # Update multiple attributes
    controller.update_attributes({
        "led_state": True,
        "brightness": 75,
        "mode": "auto",
        "lcd_message": "System Active"
    })
    
    # Display status
    controller.display_status()
    
    # Controlling device
    # controller.toggle_led()
    # controller.set_brightness(50)
    # controller.set_mode("night")
```

---

## 4. Integrated Dashboard - Kombinasi Semua Operasi

```python
import requests
from datetime import datetime
import time

class ThingsBoardDashboard:
    def __init__(self, device_id, api_key, access_token, server="thingsboard.cloud"):
        self.device_id = device_id
        self.api_key = api_key
        self.access_token = access_token
        self.server = server
        self.api_headers = {
            "X-Authorization": f"ApiKey {api_key}",
            "Content-Type": "application/json"
        }
    
    def menu(self):
        """Tampilkan main menu"""
        print("\n" + "="*50)
        print("THINGSBOARD IoT DASHBOARD")
        print("="*50)
        print("\n1. View Sensor Data")
        print("2. Send Sensor Data")
        print("3. Control Device")
        print("4. Device Status")
        print("5. Exit")
        print("\n" + "-"*50)
        
        choice = input("Select option (1-5): ")
        return choice
    
    def view_sensor_data(self):
        """Lihat data sensor"""
        print("\n[Fetching sensor data...]")
        url = f"https://{self.server}/api/plugins/telemetry/DEVICE/{self.device_id}/values/timeseries"
        params = {"keys": "temperature,humidity", "limit": 5}
        
        response = requests.get(url, headers=self.api_headers, params=params)
        if response.status_code == 200:
            data = response.json()
            print("\n✓ Latest Sensor Data:")
            for key, values in data.items():
                if values:
                    print(f"  {key}: {values[0]['value']}")
        else:
            print(f"✗ Error: {response.status_code}")
    
    def send_sensor_data(self):
        """Kirim data sensor"""
        print("\n[Send Sensor Data]")
        try:
            temp = float(input("Enter temperature (°C): "))
            humid = float(input("Enter humidity (%): "))
            
            url = f"https://{self.server}/api/v1/{self.access_token}/telemetry"
            headers = {"Content-Type": "application/json"}
            data = {"temperature": temp, "humidity": humid}
            
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                print("✓ Data sent successfully!")
            else:
                print(f"✗ Error: {response.status_code}")
        except ValueError:
            print("✗ Invalid input")
    
    def control_device(self):
        """Kontrol device"""
        print("\n[Device Control]")
        print("1. Toggle LED")
        print("2. Set Message")
        print("3. Back")
        
        choice = input("Select: ")
        url = f"https://{self.server}/api/plugins/telemetry/DEVICE/{self.device_id}/SHARED_SCOPE"
        
        if choice == "1":
            state = input("LED state (on/off): ").lower() == "on"
            data = {"led_state": state}
            response = requests.post(url, headers=self.api_headers, json=data)
            print("✓ Done" if response.status_code == 200 else f"✗ Error: {response.status_code}")
        
        elif choice == "2":
            msg = input("Enter message: ")
            data = {"lcd_message": msg}
            response = requests.post(url, headers=self.api_headers, json=data)
            print("✓ Done" if response.status_code == 200 else f"✗ Error: {response.status_code}")
    
    def run(self):
        """Jalankan dashboard"""
        while True:
            choice = self.menu()
            
            if choice == "1":
                self.view_sensor_data()
            elif choice == "2":
                self.send_sensor_data()
            elif choice == "3":
                self.control_device()
            elif choice == "4":
                print("\n[Device Status]")
                print(f"Device ID: {self.device_id}")
                print(f"Server: {self.server}")
                print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            elif choice == "5":
                print("\nGoodbye!")
                break
            else:
                print("✗ Invalid option")
            
            input("\nPress Enter to continue...")

# Jalankan dashboard
if __name__ == "__main__":
    DEVICE_ID = "aa12aac0-3636-11f1-9c01-37a7c07792f2"
    API_KEY = "tb_jo4CPe1USWzaCf_gzcL3tXe4-SDVYQmGq8DBysrHeqAzRTDojtnf7kzlzCmITsfBGdKjzw1LLXHTkvfkdn4fyg"
    ACCESS_TOKEN = "v3kmg0oatjo12qnoayyp"
    
    dashboard = ThingsBoardDashboard(DEVICE_ID, API_KEY, ACCESS_TOKEN)
    dashboard.run()
```

---

## 5. Automation Scripts

### Script 1: Periodic Data Collector
```bash
#!/bin/bash
# save as: collect_data.sh
# run every hour: 0 * * * * /path/to/collect_data.sh

cd /home/user/thingsboard
python praktikum15.py >> data_collection.log 2>&1
```

### Script 2: Health Check Monitor
```python
import requests
import time
from datetime import datetime

def check_device_health():
    """Check if device is online and responding"""
    device_id = "aa12aac0-3636-11f1-9c01-37a7c07792f2"
    api_key = "your_api_key"
    url = f"https://thingsboard.cloud/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries"
    headers = {"X-Authorization": f"ApiKey {api_key}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            print(f"[{datetime.now()}] ✓ Device is healthy")
            return True
        else:
            print(f"[{datetime.now()}] ✗ Device error: {response.status_code}")
            return False
    except Exception as e:
        print(f"[{datetime.now()}] ✗ Connection failed: {e}")
        return False

# Run every 5 minutes
while True:
    check_device_health()
    time.sleep(300)
```

---

**Advanced Usage Guide v1.0 - April 2026**
