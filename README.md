# 🚀 Robooster - SEO Automation Tools

Robooster adalah alat otomatisasi SEO yang menggabungkan bot Telegram dan dashboard web untuk membantu optimasi website secara efisien.

## 📌 Fitur Utama

### Telegram Bot
- `/analyze <url>` - Analisis SEO dasar (title, meta, heading, keyword)
- `/submit <url>` - Submit URL ke Google Indexing API
- `/report` - Laporan SEO mingguan
- `/remindme` - Pengingat update konten
- Notifikasi otomatis untuk halaman yang membutuhkan optimasi

### Web Dashboard
- Manajemen dan monitoring URL
- Penilaian SEO per halaman
- Pelacakan peringkat keyword
- Generator sitemap.xml otomatis
- Builder robots.txt interaktif
- Generator meta dengan bantuan AI

## 🛠️ Tech Stack

### Bot Telegram
- Python Telegram Bot
- APScheduler

### Backend
- FastAPI
- Pydantic
- PostgreSQL
- SQLAlchemy ORM

### Frontend
- React
- Tailwind CSS
- shadcn/ui
- Axios

### SEO Tools
- BeautifulSoup
- Google Indexing API
- Google Search Console API (opsional)

## 🔧 Konfigurasi

### Variabel Environment
```bash
# Bot Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
ADMIN_USER_ID=your_telegram_id

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/robooster

# Google API
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_PROJECT_ID=your_project_id
```

## 🚀 Cara Memulai

1. Clone repository
```bash
git clone https://github.com/username/robooster.git
cd robooster
```

2. Setup environment
```bash
cp .env.example .env
# Isi konfigurasi yang diperlukan di .env
```

3. Setup Database
```bash
# Install PostgreSQL
# Buat database baru
psql -U postgres
CREATE DATABASE robooster;
```

4. Setup Google API
- Buat project di [Google Cloud Console](https://console.cloud.google.com)
- Aktifkan Google Indexing API dan Search Console API
- Buat OAuth 2.0 credentials
- Download credentials.json

5. Jalankan bot
```bash
cd bot
pip install -r requirements.txt
python main.py
```

6. Jalankan backend
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head  # Migrasi database
uvicorn main:app --reload
```

7. Jalankan frontend
```bash
cd frontend
npm install
npm run dev
```

## 🚀 Deployment

### Backend (Fly.io)
```bash
# Install Flyctl
curl -L https://fly.io/install.sh | sh

# Login & Deploy
flyctl auth login
flyctl launch
flyctl deploy
```

### Frontend (Vercel)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

## 📝 Lisensi

MIT License

## 👥 Kontribusi

Kontribusi selalu diterima! Silakan buat issue atau pull request.