from fastapi import FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# Connect to the database with retry loop
while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='mydatabase',
            user='myuser',
            password='mypassword',
            cursor_factory=RealDictCursor  # returns rows as dictionaries
        )
        cur = conn.cursor()
        print("Database connection was successful")

        # Ensure table exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT,
            published BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cur.execute(create_table_query)
        conn.commit()

        break
    except Exception as error:
        print("Database connection failed. Retrying in 2 seconds...")
        print("Error:", error)
        time.sleep(2)




app =FastAPI()
class Post(BaseModel):
    title: str
    content: str
    published: bool=True


my_posts=[{"title": "title 1", "id": 1}, {"title": "title 2", "id": 2}]

def find_post (id):
    for p in my_posts:
        if p['id']==id: 
            return p
        

def find_post_data (id):
    for i, p in enumerate(my_posts):
        if p['id']== id:
            return i
        


@app.get("/posts")
async def get_posts():
    cur.execute(""" SELECT * FROM posts""")
    posts=cur.fetchall()
    return {"data": posts}


## Creating post request

@app.post("/createpost")
def post_api_test(new_post : Post):
    print(new_post)
    return{"new": "new_post"}


## CRUD operation

@app.get("/posts")
def get_post():
    return {"data": my_posts}


@app.post("/posts")
def new_entry(post : Post):
    post_dict= post.dict()
    post_dict['id']=randrange(1, 10000)
    my_posts.append(post_dict)
    return {'data': my_posts}


@app.get("/posts/{id}")
def get_data(id: int):
    print("my_id",id)
    data=find_post(id)
    print(data)
    return {"message": data}

@app.delete("/posts/{id}")
def delete_record (id : int, status_code=status.HTTP_204_NO_CONTENT):
    print(id)
    data=find_post_data(id)
    if data==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"ppost with id: {id} does not exist")
    my_posts.pop(data)
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_the_record(id: int, post :Post ,status_code=status.HTTP_204_NO_CONTENT):
    index=find_post_data(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"ppost with id: {id} does not exist")
    
    post_dict=post.dict()
    post_dict['id']=id
    my_posts[index]=post_dict
    return {"data": post_dict}