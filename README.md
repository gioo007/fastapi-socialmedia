# Posts API

A RESTful API built with **FastAPI** and **PostgreSQL**, featuring user authentication, JWT-based authorization, full CRUD for posts, a votes system, and database migrations via Alembic. Fully containerized with Docker and Docker Compose, with a pre-built image published on Docker Hub.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Validation | Pydantic v2 |
| Auth | JWT (OAuth2 Password Flow) |
| Password Hashing | bcrypt (via passlib) |
| Config | pydantic-settings (.env) |
| Containerization | Docker, Docker Compose |

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
- **Dynamic port binding** — reads `$PORT` at runtime for deployment platforms (Railway/Render), with a local fallback for development
- **Pre-built image on Docker Hub** — pull and run without cloning or installing dependencies locally

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
│   ├── database.py           # SQLAlchemy engine and session setup
│   ├── main.py                # App entry point, router registration
│   ├── models.py              # ORM models (User, Post, Vote)
│   ├── oauth2.py               # JWT token creation and verification
│   ├── schemas.py              # Pydantic request/response models
│   └── utils.py                # Password hashing utilities
├── .dockerignore
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml         # Local multi-container orchestration (api + db)
├── Dockerfile                 # API image build instructions
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

## Getting Started

You can run this project either with **Docker Compose** (recommended — no local Python/PostgreSQL setup needed) or manually with a local virtual environment.

### Option 1: Docker Compose (recommended)

**Prerequisites:** Docker Desktop

```bash
# Clone the repo
git clone https://github.com/gioo007/fastapi-socialmedia.git
cd fastapi-socialmedia

# Create your .env file (see Environment Variables section below)
cp .env.example .env

# Build and start the API + PostgreSQL containers
docker compose up --build
```

Migrations run inside the running API container:

```bash
docker compose exec fastapi alembic upgrade head
```

API docs available at: `http://localhost:8000/docs`

### Option 2: Pull the pre-built image from Docker Hub

```bash
docker pull giodocks/fastapi:latest
```

Run alongside your own PostgreSQL instance (see Environment Variables below for required config), or use the `docker-compose.yml` in this repo as a reference for wiring it up with a database container.

### Option 3: Manual setup (no Docker)

**Prerequisites:**
- Python 3.10+
- PostgreSQL

```bash
# Clone the repo
git clone https://github.com/gioo007/fastapi-socialmedia.git
cd fastapi-socialmedia

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Run migrations:

```bash
alembic upgrade head
```

Run the server:

```bash
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

DATABASE_HOSTNAME=postgres      # use "postgres" for Docker Compose, "localhost" for manual setup
DATABASE_PORT=5432

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **Note:** `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` are used both by the official PostgreSQL image to initialize the database, and by the API to build its database connection string — keeping a single source of truth with no duplicated values.

---

## Deployment

The API reads its listening port from the `$PORT` environment variable at runtime (with a local fallback of `8000`), making it compatible out of the box with PaaS platforms like **Railway** and **Render**, which build directly from the included `Dockerfile` and inject their own port and database configuration.

---

## Planned Additions

- pytest test suite
- CI/CD pipeline via GitHub Actions
- Deployment to Railway/Render
