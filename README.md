# Posts API

A RESTful API built with **FastAPI** and **PostgreSQL**, featuring user authentication, JWT-based authorization, full CRUD for posts, a votes system, and database migrations via Alembic. Fully containerized with Docker and Docker Compose, with a pre-built image published on Docker Hub.

**Live:** https://fastapi-socialmedia-uevd.onrender.com/docs

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL (Neon) |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Validation | Pydantic v2 |
| Auth | JWT (OAuth2 Password Flow) |
| Password Hashing | bcrypt (via passlib) |
| Config | pydantic-settings (.env) |
| Containerization | Docker, Docker Compose |
| Testing | pytest, FastAPI TestClient |
| CI/CD | GitHub Actions |
| Deployment | Render |

---

## Features

- **User registration & login** with hashed passwords
- **JWT authentication** with token expiry and protected routes
- **Post management** — create, read, update, and delete posts
- **Ownership enforcement** — users can only modify or delete their own posts
- **Votes system** — users can vote or unvote on posts (one vote per user per post)
- **Aggregated responses** — post queries return vote counts via SQL joins
- **Query parameters** — filter and limit post results
- **Schema validation** via Pydantic models with clean separation from ORM models
- **Environment-based config** via pydantic-settings and `.env`
- **Database migrations** managed with Alembic
- **Auto-generated API docs** at `/docs` (Swagger UI) and `/redoc`
- **Modular router structure** — auth, posts, users, and votes in separate routers
- **Containerized with Docker** — API and PostgreSQL run as isolated services via Docker Compose
- **Dynamic port binding** — reads `$PORT` at runtime for Render compatibility
- **Pre-built image on Docker Hub** — pull and run without cloning or installing dependencies locally
- **Automated test suite** — pytest tests covering users, posts, and votes with isolated test database
- **CI/CD pipeline** — tests gate every deployment via GitHub Actions

---

## Project Structure

```
├── alembic/                  # Database migrations
│   ├── versions/             # Migration scripts
│   └── env.py
├── apps/
│   ├── routers/
│   │   ├── auth.py           # Login endpoint
│   │   ├── posts.py          # Post CRUD endpoints
│   │   ├── users.py          # User registration and lookup
│   │   └── vote.py           # Vote endpoint
│   ├── config.py             # pydantic-settings environment config
│   ├── db.py                 # SQLAlchemy engine and session setup
│   ├── main.py               # App entry point, router registration
│   ├── models.py             # ORM models (User, Post, Vote)
│   ├── oauth2.py             # JWT token creation and verification
│   ├── schemas.py            # Pydantic request/response models
│   └── utils.py              # Password hashing utilities
├── tests/
│   ├── conftest.py           # Shared fixtures (client, session, test_user, authorized_client)
│   ├── test_users.py         # User registration and login tests
│   ├── test_posts.py         # Post CRUD and authorization tests
│   └── test_votes.py         # Vote creation and deletion tests
├── .github/
│   └── workflows/
│       ├── test.yml          # Runs pytest on push/PR to DEV
│       └── deploy.yml        # Runs pytest then deploys to Render on merge to main
├── .dockerignore
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml        # Local multi-container orchestration (api + db)
├── Dockerfile                # API image build instructions
├── requirements.txt
└── README.md
```

---

## API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/login` | Authenticate and receive JWT token |

### Users
| Method | Endpoint | Description |
|---|---|---|
| POST | `/users` | Register a new user |
| GET | `/users/{id}` | Get user by ID |

### Posts
| Method | Endpoint | Description |
|---|---|---|
| GET | `/posts` | Get all posts with vote counts |
| POST | `/posts` | Create a new post (auth required) |
| GET | `/posts/{id}` | Get post by ID with vote count |
| PUT | `/posts/{id}` | Update a post (owner only) |
| DELETE | `/posts/{id}` | Delete a post (owner only) |

### Votes
| Method | Endpoint | Description |
|---|---|---|
| POST | `/vote` | Vote or unvote on a post (auth required) |

---

## CI/CD Pipeline

Two GitHub Actions workflows:

**`test.yml`** — triggers on every push or PR to `DEV`
- Spins up a PostgreSQL 16 service container
- Runs the full pytest suite against an isolated test database
- Uses the `testing` GitHub environment for secrets

**`deploy.yml`** — triggers on merge to `main`
- Runs the full pytest suite first (same as above)
- Only if tests pass, triggers a Render deploy via deploy hook
- Uses `testing` environment for the test job and `production` environment for the deploy job

---

## Getting Started

You can run this project either with **Docker Compose** (recommended) or manually.

### Option 1: Docker Compose (recommended)

**Prerequisites:** Docker Desktop

```bash
git clone https://github.com/gioo007/fastapi-socialmedia.git
cd fastapi-socialmedia

cp .env.example .env
# fill in your values

docker compose up --build
```

Run migrations inside the container:

```bash
docker compose exec fastapi alembic upgrade head
```

API docs available at: `http://localhost:8000/docs`

### Option 2: Pull from Docker Hub

```bash
docker pull giodocks/fastapi:latest
```

### Option 3: Manual setup

**Prerequisites:** Python 3.10+, PostgreSQL

```bash
git clone https://github.com/gioo007/fastapi-socialmedia.git
cd fastapi-socialmedia

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
alembic upgrade head
uvicorn apps.main:app --reload
```

API docs available at: `http://127.0.0.1:8000/docs`

---

## Environment Variables

Create a `.env` file in the root directory (see `.env.example`):

```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_db
DATABASE_HOSTNAME=localhost    # use service name "postgres" inside Docker Compose
DATABASE_PORT=5432
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Testing

Tests use a dedicated database (`your_db_test`) that is created and torn down automatically per test via pytest fixtures.

```bash
# Create the test database once
CREATE DATABASE your_db_test;

# Run all tests
pytest

# Run with output
pytest -v -s
```

The test suite covers:

- User registration and login (including invalid credentials)
- JWT token generation and validation
- Post CRUD — create, read, update, delete
- Ownership enforcement — users cannot modify or delete other users' posts
- Authorization checks — all protected routes return 401 for unauthenticated requests
- Votes — adding, removing, duplicate vote prevention, and non-existent post handling

---

## Deployment

Deployed on **Render** with the database hosted on **Neon** (managed PostgreSQL).

The API reads `$PORT` from the environment at runtime, making it compatible with Render out of the box. Alembic migrations run automatically on every container startup before the server initializes.

Live: https://fastapi-socialmedia-uevd.onrender.com/docs