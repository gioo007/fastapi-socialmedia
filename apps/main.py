from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from random import randrange
import psycopg2 as db
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session

from .db import engine, get_db
from . import models, schemas, utils
from .routers import auth, posts, users


models.Base.metadata.create_all(bind = engine) 
app = FastAPI()
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)

#http://127.0.0.1:8000/docs for swaggerUi documentation
#http://127.0.0.1:8000/redoc for redoc documentation