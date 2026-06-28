# Posts API

A RESTful API built with **FastAPI** and **PostgreSQL**, featuring user authentication, JWT-based authorization, full CRUD for posts, a votes system, and database migrations via Alembic.

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
│   ├── main.py               # App entry point, router registration
│   ├── models.py             # ORM models (User, Post, Vote)
│   ├── oauth2.py             # JWT token creation and verification
│   ├── schemas.py            # Pydantic request/response models
│   └── utils.py              # Password hashing utilities
├── .env.example
├── .gitignore
├── alembic.ini
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

### Prerequisites

- Python 3.10+
- PostgreSQL

### Installation

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

### Run Migrations

```bash
alembic upgrade head
```

### Run the Server

```bash
uvicorn apps.main:app --reload
```

API docs available at: `http://127.0.0.1:8000/docs`

---

## Planned Additions

- pytest test suite
- Docker support