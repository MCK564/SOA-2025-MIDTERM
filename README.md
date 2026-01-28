# SOA-2025-MIDTERM — iBanking Tuition Payment Subsystem 💳🎓

A service-oriented **tuition payment subsystem** for an iBanking application. This repository appears to be a Python-based API service with modular folders for `api/`, `services/`, `models/`, `schemas/`, `core/`, and includes Docker artifacts (`Dockerfile`, `docker-compose.yml`) plus a SQL script `bank.sql` for database setup. citeturn1view0

> Repo: https://github.com/MCK564/SOA-2025-MIDTERM  
> Description on GitHub: *"ibanking application - tuition payment subsystem."*

---

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Tech Stack (expected)](#tech-stack-expected)
- [Prerequisites](#prerequisites)
- [Run with Docker](#run-with-docker)
- [Run Locally (without Docker)](#run-locally-without-docker)
- [Configuration](#configuration)
- [Database](#database)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview
This project implements the backend side of a **tuition payment flow** inside an iBanking system, typically involving:
- Student tuition information lookup
- Payment initiation
- Transaction recording
- Status update / reconciliation

The repo contains a ready-to-run setup using **Docker** and a database initialization script (`bank.sql`). citeturn1view0

---

## Project Structure
Top-level layout as shown in the repository: citeturn1view0

```
SOA-2025-MIDTERM/
  api/                 # API routes (controllers/routers)
  services/            # Business logic layer
  models/              # ORM models / DB entities
  schemas/             # Request/response schemas (DTOs)
  core/                # core settings, security, shared config
  utils/               # helper utilities
  tests/               # tests
  main.py              # application entrypoint
  dependencies.py      # dependency injection / shared dependencies
  bank.sql             # database schema/seed
  requirements.txt     # Python dependencies
  Dockerfile           # container build
  docker-compose.yml   # container orchestration
```

> Notes:
> - Exact filenames inside folders may vary; the structure above is from the repo root listing. citeturn1view0

---

## Tech Stack (expected)
Based on the presence of `main.py`, `schemas/`, and `dependencies.py`, this project is commonly structured like a **FastAPI** (or similar) service. (If you want, paste `requirements.txt` here and I’ll make this section 100% exact.)

---

## Prerequisites
### Option A — Docker (recommended)
- Docker + Docker Compose

### Option B — Local Python
- Python 3.10+ (recommended)
- pip / venv

---

## Run with Docker
The repository includes both `Dockerfile` and `docker-compose.yml`. citeturn1view0

### 1) Clone
```bash
git clone https://github.com/MCK564/SOA-2025-MIDTERM.git
cd SOA-2025-MIDTERM
```

### 2) Start services
```bash
docker compose up -d --build
```

### 3) Verify containers
```bash
docker compose ps
```

### 4) View logs (if needed)
```bash
docker compose logs -f
```

---

## Run Locally (without Docker)

### 1) Create & activate virtual environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Setup database
Use the provided `bank.sql` to create schema and seed data. citeturn1view0  
How you import depends on your DB engine (MySQL/Postgres/etc.). Typical patterns:

**MySQL example**
```bash
mysql -u root -p -e "CREATE DATABASE bank;"
mysql -u root -p bank < bank.sql
```

### 4) Run the API
```bash
python main.py
```

> If this project uses an ASGI server (common), you might run something like:
> `uvicorn main:app --reload`
> (Check `main.py` for the exact command.)

---

## Configuration
Typical things you may need to configure (depending on your code in `core/` and `.env` usage):
- Database connection string (host, port, db name, username, password)
- App port
- JWT/secret keys (if auth is included)
- External bank/payment sandbox configs (if any)

If the repo already includes a sample `.env`, copy it:
```bash
cp .env.example .env
```

---

## Database
The repo includes `bank.sql` which is intended to initialize the banking database schema (and possibly seed data). citeturn1view0

Recommended:
- Keep SQL scripts versioned
- Consider adding migration tooling (Alembic) if the schema evolves

---

## Testing
A `tests/` folder exists in the project. citeturn1view0  
Run tests (common commands):
```bash
pytest
```

If you use `unittest`:
```bash
python -m unittest
```

---

## Troubleshooting
### Container can’t connect to DB
- Make sure DB container is healthy: `docker compose ps`
- Confirm credentials match your environment variables / compose file
- Check logs: `docker compose logs -f`

### Import SQL fails
- Ensure the target DB exists
- Ensure correct DB engine (MySQL vs Postgres syntax differs)
- Try importing via a GUI tool (MySQL Workbench / DBeaver)

### Port already in use
- Stop old containers or change exposed ports in `docker-compose.yml`

---

## License
Add a license if you plan to publish/reuse this project publicly.
