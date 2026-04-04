# 💰 FinTrack API

REST API untuk manajemen keuangan pribadi — tracking pemasukan, pengeluaran, budget, dan laporan bulanan.

## 🚀 Live Demo
**Base URL:** https://fintrack-api-test.up.railway.app

**Swagger UI:** https://fintrack-api-test.up.railway.app/docs

## 🛠 Tech Stack
- **FastAPI** — Modern Python web framework
- **PostgreSQL** — Database (hosted on Railway)
- **SQLAlchemy 2.0** — Async ORM
- **Alembic** — Database migrations
- **JWT** — Authentication
- **Railway** — Cloud deployment

## 📌 Features
- 🔐 Register & Login dengan JWT token
- 📂 Manajemen kategori pengeluaran
- 💸 CRUD transaksi (income & expense)
- 🎯 Set budget per kategori per bulan
- 📊 Laporan bulanan (income, expense, balance)

## 📖 API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/register | Register user baru |
| POST | /auth/login | Login & dapat JWT token |

### Categories
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /categories/ | Lihat semua kategori |
| POST | /categories/ | Buat kategori baru |

### Expenses
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /expenses/ | Lihat semua transaksi |
| POST | /expenses/ | Tambah transaksi baru |
| PUT | /expenses/{id} | Edit transaksi |
| DELETE | /expenses/{id} | Hapus transaksi |

### Budgets & Report
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /budgets/ | Lihat semua budget |
| POST | /budgets/ | Buat budget baru |
| GET | /budgets/report/{month} | Laporan bulanan |

## 🏃 Run Locally
```bash
# Clone repo
git clone https://github.com/muhammarbachdar/fintrack-api.git
cd fintrack-api

# Install dependencies
pip install -r requirements.txt

# Setup .env
DATABASE_URL=postgresql+asyncpg://...

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

## 👤 Author
M. Ammar Ramadan Bachdar