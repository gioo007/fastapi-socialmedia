from fastapi import FastAPI
from .routers import auth, posts, users, vote 

app = FastAPI()
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World"}

#http://127.0.0.1:8000/docs for swaggerUi documentation
#http://127.0.0.1:8000/redoc for redoc documentation