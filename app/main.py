import time
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg
import json

app = FastAPI()

class PostSchema(BaseModel):
    title: str
    content: str
    published: bool = True

ctr = 0
conf_filepath = 'db_config/db_conf.json'

def read_config(file_path):
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    return config

config = read_config(conf_filepath)

database_config = config['database']

host = database_config['host']
dbname = database_config['dbname']
user = database_config['user']
password = database_config['password']

while True:
    try:
        connection = psycopg.connect(host=host, dbname=dbname, user=user, 
                                    password=password)
        cursor = connection.cursor()
        print("DB connection successful")
        ctr = 0
        break
    except Exception as error:
        print("DB connection failed\nError: ", error)
        time.sleep(2)
        ctr += 1
        if(ctr == 10):
            print("DB connection failed 10 times. Exiting")
            exit()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/posts")
def read_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post : PostSchema):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                    (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    connection.commit()
    return {"new_post": new_post}


@app.get("/posts/{post_id}")
def get_post(post_id: int): 
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (post_id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=404, detail = f"Post id : {post_id} not found")
    return {"data": post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id : int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(post_id),))
    deleted_post = cursor.fetchone()
    connection.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post {post_id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
def update_post(post_id : int, new_post : PostSchema):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (new_post.title, new_post.content, new_post.published, post_id))
    updated_post = cursor.fetchone()
    connection.commit()
    if updated_post == None:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found")
    return {"data": updated_post}
