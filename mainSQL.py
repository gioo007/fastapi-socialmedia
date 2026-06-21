from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2 as db
from psycopg2.extras import RealDictCursor
import time

#psycopg2 and MySQL are db drivers for python


app = FastAPI()

while True:
    try:
        #hard coded db info, will later change in production
        conn = db.connect(
            host = "localhost", 
            database = "fastapi db", 
            user = "postgres", 
            password = "admin",
            cursor_factory = RealDictCursor
            )
        cursor = conn.cursor()
        print("Connection successful")
        break

    except Exception as e:
        print(f"Connection to database failed\nError: {e}")
        time.sleep(2)


class Post(BaseModel):
    title: str
    content: str
    published: bool = False


@app.get("/")
async def root(): 
    return {"message": "Welcome to my API!"}


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM public.posts ORDER BY id ASC")
    # for row in cursor:
    # ---
    posts = cursor.fetchall()
    return {"data": posts}


@app.get("/posts/latest")
def get_latest_post():
    cursor.execute("Select * from posts order by id desc")
    latest_post = cursor.fetchone()
    if latest_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    return {"data": latest_post}


@app.get("/posts/{id}") #id automatically extracted and added to function
def get_post(id: int, response: Response): #can also use response: Response to modify the response object directly
    cursor.execute("Select * from posts where id = %s", (str(id),))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")
    return {"data": post}


@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(post: Post): 
    cursor.execute("INSERT INTO posts (title, content, published, created) VALUES (%s, %s, %s, NOW()) RETURNING *"
                   , (post.title, post.content, post.published))
    posted = cursor.fetchone()
    conn.commit()
    return {
        "data": posted 
    }

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
                   (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")
    return {"data": updated_post}

@app.patch("/posts/{id}")
def patch_post(id: int, post: Post):
    cursor.execute("Update posts set title = ")
    patched_post = cursor.fetchone()
    conn.commit()
    if patched_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")
    return {"data": patched_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("Delete from posts where id = %s RETURNING *", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")
    return {"data": deleted_post}


