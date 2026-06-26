from fastapi import FastAPI
from .db import engine
from . import models
from .routers import auth, posts, users


models.Base.metadata.create_all(bind = engine) 
app = FastAPI()
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)

#http://127.0.0.1:8000/docs for swaggerUi documentation
#http://127.0.0.1:8000/redoc for redoc documentation