# Job Application Tracking System

A backend REST API built with **FastAPI** and **PostgreSQL** to manage job application workflows, statuses, and deadlines with full audit history.

## Tech Stack

- **FastAPI** - Web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **JWT (python-jose)** - Authentication
- **Pydantic** - Data validation
- **Passlib (bcrypt)** - Password hashing

## Features

- User registration and login with JWT authentication
- Full CRUD for job applications
- Status workflow tracking: `applied` → `phone_screen` → `interview` → `offer` → `accepted` / `rejected` / `withdrawn`
- Persistent status history with timestamps for traceability
- Deadline tracking
- Filter applications by status with pagination
- Each user can only access their own data

## Project Structure

```
app/
├── main.py                 # FastAPI entry point
├── config.py               # Environment-based settings
├── database.py             # SQLAlchemy engine and session
├── dependencies.py         # JWT auth dependency
├── models/                 # SQLAlchemy ORM models
│   ├── user.py
│   ├── job_application.py
│   └── status_history.py
├── schemas/                # Pydantic request/response schemas
│   ├── user.py
│   ├── job_application.py
│   └── status_history.py
├── routers/                # API route handlers
│   ├── auth.py
│   └── job_applications.py
└── services/               # Business logic layer
    ├── auth.py
    └── job_application.py
```

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create a new account |
| POST | `/auth/login` | Login and get JWT token |
| GET | `/auth/me` | Get current user profile |

### Job Applications
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/applications/` | Create a new application |
| GET | `/applications/` | List all applications (filter by `?status=`, pagination) |
| GET | `/applications/{id}` | Get application detail with status history |
| PATCH | `/applications/{id}` | Update application fields |
| PATCH | `/applications/{id}/status` | Change status (recorded in history) |
| DELETE | `/applications/{id}` | Delete an application |

## Setup

### Prerequisites
- Python 3.11+
- PostgreSQL

### Installation

```bash
# Clone the repository
git clone https://github.com/KTH-Sys/JobAppTrackingSystem.git
cd JobAppTrackingSystem

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database URL and secret key

# Create the database
createdb job_tracker

# Run migrations
alembic revision --autogenerate -m "initial"
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs`

## Database Schema

```
users ──1:N── job_applications ──1:N── status_history
```

- **users** - Stores accounts with hashed passwords
- **job_applications** - Stores application details and current status
- **status_history** - Audit trail recording every status change with timestamps
