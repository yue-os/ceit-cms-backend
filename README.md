# CEIT CMS Backend

> **⚠️ WARNING: DO NOT PUSH DIRECTLY TO THE MAIN BRANCH ⚠️**
>
> Always create a feature branch and submit a pull request for review.

---

## Project Structure

```
ceit-cms-backend/
├── alembic/                    # Database migrations
│   ├── versions/               # Migration scripts
│   ├── env.py                  # Alembic environment config
│   └── script.py.mako          # Migration template
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/      # API route handlers
│   │       │   └── auth.py
│   │       ├── dependencies.py # Dependency injection
│   │       └── router.py       # API router
│   ├── core/
│   │   ├── config.py           # App configuration
│   │   ├── database.py         # Database connection
│   │   └── security.py         # Auth & security utils
│   ├── middleware/
│   │   └── cors.py             # CORS middleware
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── article.py
│   │   ├── base.py
│   │   ├── permission.py
│   │   ├── role.py
│   │   └── user.py
│   ├── repositories/           # Data access layer
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── user.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   └── auth.py
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   └── auth_service.py
│   └── main.py                 # FastAPI app entry point
├── scripts/
│   └── seed.py                 # Database seeding script
├── .env                        # Environment variables (not in git)
├── .env.example                # Example environment variables
├── alembic.ini                 # Alembic configuration
└── requirements.txt            # Python dependencies
```

---

## Setup Guide

### 1. Create Virtual Environment

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```powershell
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Copy the example env file and configure it:

```bash
cp .env.example .env
```

Then edit `.env` with your database credentials and secrets.

### 4. Database Migrations

**Create a new migration:**

```bash
# Linux/macOS
alembic revision --autogenerate -m "Migration message"

# Windows
alembic revision --autogenerate -m "Migration message"
```

**Apply migrations:**

```bash
alembic upgrade head
```

**Rollback last migration:**

```bash
alembic downgrade -1
```

### 5. Seed Database

```bash
python scripts/seed.py
```

### 6. Run Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

API docs: `http://localhost:8000/docs`
