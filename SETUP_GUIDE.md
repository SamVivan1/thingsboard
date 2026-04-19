# 📋 Setup Guide - ThingsBoard IoT Project

## Panduan Instalasi dan Konfigurasi Lengkap

---

## 1. Persiapan Awal

### Persyaratan Hardware
- Komputer dengan koneksi internet
- Python 3.6+
- Terminal/Command Prompt

### Persyaratan Software
- Python dan pip (package manager)
- Git (opsional, untuk version control)
- Text editor atau IDE (VS Code, PyCharm, dll)

---

## 2. Instalasi Python dan Dependencies

### Step 1: Verifikasi Python Installation
```bash
# Periksa versi Python
python --version
# atau
python3 --version

# Output yang diharapkan: Python 3.6 atau lebih baru
```

### Step 2: Install Library Requirements
```bash
# Instalasi requests library
pip install requests

# Atau install dari requirements.txt (jika ada)
pip install -r requirements.txt
```

### Step 3: Verifikasi Installation
```bash
python -c "import requests; print(requests.__version__)"
# Output: 2.x.x (versi requests)
```

---

## 3. Setup ThingsBoard Cloud Account

### Step 1: Buat Akun
1. Kunjungi https://thingsboard.cloud
2. Klik "Sign Up"
3. Isi form registrasi dengan email dan password
4. Verifikasi email Anda
5. Login ke dashboard

### Step 2: Tambahkan Device
1. Di dashboard, klik **Devices** (menu kiri)
2. Klik tombol **"+"** untuk menambah device
3. Isi informasi:
   - **Name**: Nama device (contoh: "Sensor Ruang 1")
   - **Type**: Pilih tipe device atau buat baru
   - **Device Profile**: Pilih profil yang sesuai
4. Klik **Add**

### Step 3: Ambil Access Token
1. Di list Devices, klik device Anda
2. Buka tab **Details**
3. Copy **Access token** (untuk praktikum16.py)
4. Simpan di tempat aman

---

## 4. Mendapatkan API Key

### Untuk Praktikum 15 dan 17

1. **Login ke ThingsBoard**
2. **Klik Avatar** (kanan atas) → **Settings**
3. **Tab API Tokens** atau **Settings**
4. **Create New Token** atau gunakan existing API Key
5. Copy API Key dan Device ID

### Format yang Dibutuhkan
```
API_KEY: tb_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DEVICE_ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

---

## 5. Konfigurasi Script

### Praktikum 15 - Baca Data Telemetri

**File:** `praktikum15.py`

```python
# Ganti dengan nilai Anda
SERVER = "thingsboard.cloud"
DEVICE_ID = "YOUR_DEVICE_ID"           # Ganti dengan Device ID Anda
API_KEY = "YOUR_API_KEY"                # Ganti dengan API Key Anda
```

**Cara mendapatkan DEVICE_ID:**
1. Buka Device di ThingsBoard
2. Cari bagian **ID** (biasanya di bagian atas atau Details tab)
3. Copy nilai tersebut

### Praktikum 16 - Kirim Data Sensor

**File:** `praktikum16.py`

```python
# Ganti dengan nilai Anda
SERVER = "thingsboard.cloud"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"     # Ganti dengan Access Token
```

**Cara mendapatkan ACCESS_TOKEN:**
1. Buka Device di ThingsBoard
2. Tab **Details**
3. Copy **Access token**

### Praktikum 17 - Kelola Attributes

**File:** `praktikum17.py`

```python
# Ganti dengan nilai Anda yang sama seperti praktikum15.py
SERVER = "thingsboard.cloud"
DEVICE_ID = "YOUR_DEVICE_ID"
API_KEY = "YOUR_API_KEY"
```

---

## 6. Testing Konfigurasi

### Test 1: Koneksi Internet
```bash
# Test koneksi ke ThingsBoard server
ping thingsboard.cloud
```

### Test 2: Python Environment
```bash
# Pastikan requests library terpasang
python -c "import requests; print('OK')"
```

### Test 3: Jalankan Praktikum 15 (Read Data)
```bash
python praktikum15.py
```

**Expected Output:**
```json
{
  "temperature": [...],
  "humidity": [...]
}
```

Jika berhasil, Anda siap untuk tahap berikutnya!

---

## 7. Troubleshooting Setup

### Error: "ModuleNotFoundError: No module named 'requests'"

**Solusi:**
```bash
# Reinstall requests
pip install --upgrade requests

# Atau gunakan pip3 jika pip tidak berfungsi
pip3 install requests
```

### Error: "401 Unauthorized"

**Kemungkinan Penyebab & Solusi:**
1. API Key/Token salah
   - Copy lagi dari ThingsBoard dengan hati-hati
   - Pastikan tidak ada extra space/character
   
2. Token expired
   - Generate token baru di ThingsBoard
   - Update script dengan token baru

3. Header format salah
   - Pastikan `X-Authorization: ApiKey {VALUE}` (jangan `Bearer`)

### Error: "404 Not Found"

**Solusi:**
1. Periksa DEVICE_ID
2. Pastikan device sudah ada di ThingsBoard
3. Device ID harus format UUID: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

### Error: "Connection timeout"

**Solusi:**
```bash
# Periksa koneksi internet
ping 8.8.8.8

# Periksa bisa akses ThingsBoard
curl https://thingsboard.cloud/api/v1/health
```

---

## 8. Setup Environment Variables (Opsional tapi Recommended)

### Mengapa Environment Variables?
- Lebih aman (kredensial tidak hardcoded)
- Mudah untuk development dan production
- Compliance dengan security best practices

### Setup di Linux/Mac

**Buat file `.env`:**
```bash
cat > .env << EOF
THINGSBOARD_SERVER=thingsboard.cloud
DEVICE_ID=your_device_id
API_KEY=your_api_key
ACCESS_TOKEN=your_access_token
EOF
```

**Update script untuk membaca `.env`:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

SERVER = os.getenv("THINGSBOARD_SERVER", "thingsboard.cloud")
DEVICE_ID = os.getenv("DEVICE_ID")
API_KEY = os.getenv("API_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
```

**Install python-dotenv:**
```bash
pip install python-dotenv
```

### Setup di Windows

**Buat file `.env` atau set environment variable:**
```bash
set THINGSBOARD_SERVER=thingsboard.cloud
set DEVICE_ID=your_device_id
set API_KEY=your_api_key
```

---

## 9. First Run Checklist

- [ ] Python 3.6+ terinstall
- [ ] `requests` library terinstall
- [ ] ThingsBoard account sudah dibuat
- [ ] Device sudah ditambahkan
- [ ] API Key & Device ID sudah diperoleh
- [ ] Access Token sudah diperoleh
- [ ] Script sudah dikonfigurasi dengan kredensial
- [ ] Praktikum15.py berhasil dijalankan
- [ ] Praktikum16.py berhasil mengirim data
- [ ] Praktikum17.py berhasil update attributes

---

## 10. Next Steps

Setelah setup berhasil:
1. Baca [README.md](README.md) untuk dokumentasi lengkap
2. Experiment dengan modifikasi data di praktikum16.py
3. Buat lebih banyak attributes di praktikum17.py
4. Integrate dengan sensor hardware
5. Build automation scripts

---

**Setup Guide v1.0 - April 2026**
