from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2 as db
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


#example data stored in memory, as a list of dictionaries
my_posts = [{"title": "dogs", "content": "dogs are great", "id": 1}, {"title": "cats", "content": "cats are great", "id": 2}]

#schema for the post data using pydantic
#fastapi will validate data using pydantic models
class Post(BaseModel): #extends BaseModel from pydantic
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None


#==========================================
#Get
#==========================================

@app.get("/helloWorld")
async def hello_world():
    return {"message": "Hello World!"}

#get is just one of the HTTP methods
#the / is the root path/endpoint of the API, "the address" where the API is accessed
@app.get("/") #decorator to define a route/endpoint for people to call at
#root function, name doesnt matter, keep decriptive
async def root(): #async to allow for asynchronous operations (optional tho if you dont want async)
    return {"message": "Welcome to my API!"}


#define a func, its return, and the http method
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    if post:
        return {"latest post": post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")

@app.get("/posts/{id}") #id automatically extracted and added to function
def get_post(id: int, response: Response): #can also use response: Response to modify the response object directly
    post = find_post(id)
    if post is None:
        response.status_code = status.HTTP_404_NOT_FOUND #status is imported above
        return {"message": "Post not found"}
    return {"post detail": post}



#==========================================
#Post
#==========================================
def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None

#json body, unvalidated, not recommended
@app.post("/createpost")
def create_post2(body: dict = Body(...)): #type dict, ... means required, could be optional (None)
    return {
        f"title {body["title"]}",
        f"content {body['content']}"
    }

@app.post("/post", status_code=status.HTTP_201_CREATED) #changes default status code
def create_post(post: Post): #can easily access each already validated attribute
    postDict = post.dict()  # convert pydantic model to python dict if needed
    postDict['id'] = randrange(0, 1000000)  # add an id to the post
    my_posts.append(postDict)



@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    for index, p in enumerate(my_posts):
        if p["id"] == id:
            my_posts[index] = post.dict()
            my_posts[index]["id"] = id
            return {"data": my_posts[index]}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")
    my_posts.remove(post)

#put requires the entire object to update, patch only requires the fields to update
#http://127.0.0.1:8000/docs for swaggeerUi documentation
#http://127.0.0.1:8000/redoc for redoc documentation