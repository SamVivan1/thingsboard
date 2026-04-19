# Dokumentasi Project ThingsBoard IoT Integration

## 📋 Daftar Isi
1. [Pengenalan Project](#pengenalan-project)
2. [Prasyarat dan Setup](#prasyarat-dan-setup)
3. [Struktur Project](#struktur-project)
4. [Modul-Modul](#modul-modul)
5. [Konfigurasi API](#konfigurasi-api)
6. [Cara Penggunaan](#cara-penggunaan)
7. [Referensi API](#referensi-api)

---

## 🎯 Pengenalan Project

Project ini merupakan implementasi integrasi IoT dengan platform **ThingsBoard Cloud**. Project ini mendemonstrasikan tiga operasi utama dalam komunikasi IoT:

- **Membaca Data Telemetri** (praktikum15.py): Mengambil data sensor yang sudah tersimpan
- **Mengirim Data Sensor** (praktikum16.py): Mengirimkan data telemetri real-time dari perangkat
- **Mengelola Attributes** (praktikum17.py): Membuat dan memperbarui atribut perangkat seperti status LED dan pesan LCD

### Teknologi yang Digunakan
- **Platform**: ThingsBoard Cloud (thingsboard.cloud)
- **Bahasa**: Python 3
- **Library**: `requests` (HTTP client)
- **API**: ThingsBoard REST API v1

---

## 🛠️ Prasyarat dan Setup

### Persyaratan Sistem
- Python 3.6 atau lebih baru
- Koneksi internet yang stabil
- Akun di [ThingsBoard Cloud](https://thingsboard.cloud)

### Instalasi Dependencies

```bash
# Install library requests
pip install requests

# Atau menggunakan requirements.txt
pip install -r requirements.txt
```

### Konfigurasi Kredensial

Sebelum menjalankan script, pastikan Anda memiliki:
1. **Device ID**: Identifier unik untuk perangkat IoT Anda
2. **API Key atau Access Token**: Kredensial autentikasi untuk ThingsBoard
3. **Server Address**: URL server ThingsBoard (default: thingsboard.cloud)

> ⚠️ **PERHATIAN KEAMANAN**: Jangan commit kredensial ke repository. Pertimbangkan menggunakan environment variables atau file `.env`.

---

## 📁 Struktur Project

```
thingsboard/
├── README.md                    # Dokumentasi project (file ini)
├── praktikum15.py             # Script membaca data telemetri
├── praktikum16.py             # Script mengirim data sensor
└── praktikum17.py             # Script mengelola shared attributes
```

---

## 📚 Modul-Modul

### 1. **praktikum15.py** - Membaca Data Telemetri

#### Deskripsi
Script ini digunakan untuk mengambil data telemetri (sensor data) dari perangkat yang sudah terekam di ThingsBoard Cloud.

#### Fitur Utama
- Mengambil data time-series dari device tertentu
- Autentikasi menggunakan API Key
- Mendisplay data dalam format JSON

#### Konfigurasi
```python
SERVER = "thingsboard.cloud"
DEVICE_ID = "aa12aac0-3636-11f1-9c01-37a7c07792f2"
API_KEY = "tb_jo4CPe1USWzaCf_gzcL3tXe4-SDVYQmGq8DBysrHeqAzRTDojtnf7kzlzCmITsfBGdKjzw1LLXHTkvfkdn4fyg"
```

#### Endpoint API
```
GET https://thingsboard.cloud/api/plugins/telemetry/DEVICE/{DEVICE_ID}/values/timeseries
Header: X-Authorization: ApiKey {API_KEY}
```

#### Output Contoh
```json
{
  "temperature": [{"ts": 1624089600000, "value": "23.5"}],
  "humidity": [{"ts": 1624089600000, "value": "65"}],
  "pressure": [{"ts": 1624089600000, "value": "1013"}]
}
```

#### Cara Menjalankan
```bash
python praktikum15.py
```

---

### 2. **praktikum16.py** - Mengirim Data Sensor

#### Deskripsi
Script ini mengirimkan data sensor (telemetri) real-time ke ThingsBoard Cloud. Digunakan ketika perangkat IoT ingin melaporkan data sensor mereka.

#### Fitur Utama
- Mengirim data sensor (temperature, humidity) ke cloud
- Autentikasi menggunakan Access Token
- Support untuk mengirim multiple sensor values sekaligus

#### Konfigurasi
```python
SERVER = "thingsboard.cloud"
ACCESS_TOKEN = "v3kmg0oatjo12qnoayyp"
```

#### Endpoint API
```
POST https://thingsboard.cloud/api/v1/{ACCESS_TOKEN}/telemetry
Content-Type: application/json

{
  "temperature": 45,
  "humidity": 78
}
```

#### Parameter Data
| Nama Field | Tipe | Deskripsi |
|-----------|------|-----------|
| `temperature` | Number | Nilai suhu dalam Celsius |
| `humidity` | Number | Nilai kelembaban dalam persen (%) |

#### Cara Menjalankan
```bash
python praktikum16.py
```

#### Output
```
kirim data done
```

#### Modifikasi untuk Data Berbeda
Anda dapat mengubah data sensor yang dikirim dengan memodifikasi dictionary `data_sensor`:

```python
data_sensor = {
    "temperature": 45,
    "humidity": 78,
    "pressure": 1013.25,
    "co2": 420
}
```

---

### 3. **praktikum17.py** - Mengelola Shared Attributes

#### Deskripsi
Script ini membuat atau memperbarui shared attributes dari perangkat. Attributes adalah metadata yang dapat dikontrol dari server dan diakses oleh perangkat.

#### Fitur Utama
- Membuat/update shared attributes
- Support untuk boolean dan string values
- Autentikasi menggunakan API Key

#### Konfigurasi
```python
SERVER = "thingsboard.cloud"
DEVICE_ID = "aa12aac0-3636-11f1-9c01-37a7c07792f2"
API_KEY = "tb_jo4CPe1USWzaCf_gzcL3tXe4-SDVYQmGq8DBysrHeqAzRTDojtnf7kzlzCmITsfBGdKjzw1LLXHTkvfkdn4fyg"
```

#### Endpoint API
```
POST https://thingsboard.cloud/api/plugins/telemetry/DEVICE/{DEVICE_ID}/SHARED_SCOPE
Header: X-Authorization: ApiKey {API_KEY}
Header: Content-Type: application/json

{
  "led_state": false,
  "lcd_message": "hello dunia"
}
```

#### Jenis Attributes
| Scope | Deskripsi | Use Case |
|-------|-----------|----------|
| **SHARED_SCOPE** | Dapat diakses oleh client dan server | Kontrol device (LED, message) |
| **SERVER_SCOPE** | Hanya bisa diakses server | Data internal/private |
| **CLIENT_SCOPE** | Hanya bisa diakses client | Data device-specific |

#### Contoh Attribute
```python
data_attribute = {
    "led_state": True,           # Boolean
    "lcd_message": "hello dunia", # String
    "brightness": 85,            # Number
    "mode": "auto"               # String
}
```

#### Cara Menjalankan
```bash
python praktikum17.py
```

#### Output
```
buat/update done
```

---

## 🔑 Konfigurasi API

### Autentikasi

ThingsBoard Cloud mendukung dua metode autentikasi:

#### 1. **API Key Authentication** (Praktikum 15 & 17)
- Lebih fleksibel untuk server-to-server communication
- Header: `X-Authorization: ApiKey {API_KEY}`
- Use case: Admin operations, bulk data retrieval

```python
headers = {
    "X-Authorization": f"ApiKey {API_KEY}"
}
```

#### 2. **Access Token** (Praktikum 16)
- Untuk device-to-server communication
- Use case: Perangkat mengirim data telemetri
- URL: `/api/v1/{ACCESS_TOKEN}/telemetry`

```python
url = f"https://{SERVER}/api/v1/{ACCESS_TOKEN}/telemetry"
```

### Mendapatkan Kredensial

**Untuk Device Access Token:**
1. Login ke [ThingsBoard Cloud](https://thingsboard.cloud)
2. Buka menu **Devices**
3. Pilih device Anda
4. Tab **Details** → Copy **Access token**

**Untuk API Key:**
1. Login ke ThingsBoard Cloud
2. Buka menu **Settings** → **API Keys**
3. Create new API Key atau copy existing key

---

## 💻 Cara Penggunaan

### Scenario 1: Monitoring Data Sensor
```bash
# Jalankan praktikum15.py untuk melihat data sensor terbaru
python praktikum15.py
```

### Scenario 2: Device Mengirim Data
```bash
# Jalankan praktikum16.py untuk mengirim data sensor
python praktikum16.py
```

### Scenario 3: Mengontrol Device
```bash
# Jalankan praktikum17.py untuk set LED status atau message
python praktikum17.py
```

### Menjalankan Semua Script
```bash
# Run all modules
python praktikum15.py && python praktikum16.py && python praktikum17.py
```

### Automation dengan Cron Job
```bash
# Kirim data setiap 5 menit
*/5 * * * * cd /path/to/thingsboard && python praktikum16.py

# Check data setiap jam
0 * * * * cd /path/to/thingsboard && python praktikum15.py
```

---

## 📖 Referensi API

### Dokumentasi Resmi
- [ThingsBoard Cloud REST API Documentation](https://thingsboard.io/docs/api/)
- [Device API Reference](https://thingsboard.io/docs/reference/rest-api/)
- [Telemetry Upload API](https://thingsboard.io/docs/reference/http-api/)

### HTTP Methods
| Method | Penggunaan | Script |
|--------|-----------|--------|
| `GET` | Membaca data (Read) | praktikum15.py |
| `POST` | Mengirim/membuat data | praktikum16.py, praktikum17.py |
| `PUT` | Memperbarui data | - |
| `DELETE` | Menghapus data | - |

### Status Code API
| Code | Arti |
|------|------|
| `200` | OK - Request berhasil |
| `400` | Bad Request - Format request salah |
| `401` | Unauthorized - Autentikasi gagal |
| `403` | Forbidden - Akses ditolak |
| `404` | Not Found - Resource tidak ditemukan |
| `500` | Server Error - Error di server |

---

## 🐛 Troubleshooting

### Error: 401 Unauthorized
**Solusi:**
- Periksa API Key/Access Token
- Pastikan token belum expired
- Verifikasi Header autentikasi sudah benar

### Error: 404 Not Found
**Solusi:**
- Periksa DEVICE_ID yang digunakan
- Pastikan device sudah didaftarkan di ThingsBoard

### Connection Timeout
**Solusi:**
- Periksa koneksi internet
- Pastikan server thingsboard.cloud dapat diakses
- Coba tambah timeout pada requests

```python
response = requests.get(url, headers=headers, timeout=10)
```

### Data Tidak Terkirim
**Solusi:**
- Verifikasi format JSON
- Pastikan Content-Type header benar
- Cek payload data structure

---

## 📝 Catatan Pengembangan

- Semua script menggunakan library `requests` untuk HTTP communication
- Format timestamp menggunakan milliseconds (Unix timestamp × 1000)
- Semua komunikasi dilakukan via HTTPS untuk keamanan
- Rate limiting mungkin diterapkan oleh ThingsBoard untuk API calls

---

## 📄 Lisensi

Project ini merupakan hasil praktikum IoT dengan ThingsBoard Cloud.

---

**Last Updated:** April 2026
**Version:** 1.0
