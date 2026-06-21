# Posts API

A RESTful API built with **FastAPI** and **PostgreSQL**, featuring user authentication, JWT-based authorization, and full CRUD functionality for posts.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Validation | Pydantic v2 |
| Auth | JWT (OAuth2 Password Flow) |
| Password Hashing | bcrypt (via passlib) |

---

## Features

- **User registration & login** with hashed passwords
- **JWT authentication** with token expiry and protected routes
- **Post management** — create, read, update, and delete posts
- **Ownership enforcement** — users can only modify their own posts
- **Schema validation** via Pydantic models with clean separation from ORM models
- **Auto-generated API docs** at `/docs` (Swagger UI) and `/redoc`
- **Modular router structure** — auth and posts split into separate routers

---

## Project Structure

```
app/
├── main.py           # App entry point, router registration
├── database.py       # SQLAlchemy engine and session setup
├── models.py         # ORM models (User, Post)
├── schemas.py        # Pydantic request/response models
├── oauth2.py         # JWT token creation and verification
├── utils.py          # Password hashing utilities
└── routers/
    ├── auth.py       # Login endpoint
    ├── posts.py      # Post CRUD endpoints
    └── users.py      # User registration and lookup
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
| GET | `/posts` | Get all posts |
| POST | `/posts` | Create a new post (auth required) |
| GET | `/posts/{id}` | Get post by ID |
| PUT | `/posts/{id}` | Update a post (owner only) |
| DELETE | `/posts/{id}` | Delete a post (owner only) |

---

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL

### Installation

```bash
# Clone the repo
git clone https://github.com/gioo007/fastapi-socialmedia.git
cd posts-api

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_NAME=your_db
DATABASE_USERNAME=your_user
DATABASE_PASSWORD=your_password
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Run the Server

```bash
uvicorn app.main:app --reload
```

API docs available at: `http://127.0.0.1:8000/docs`

---

## Planned Additions

- Votes/likes on posts
- SQL joins for aggregated post data
- Alembic database migrations
- pytest test suite
- Docker support
