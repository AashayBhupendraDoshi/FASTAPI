# Older version that employs psycopg to directly
# interact with Postgresql database using sql commands
# New version uses sqlalchemy ORM to interact with PostgreSQL


from asyncio.windows_events import NULL
from distutils.log import error
from sqlite3 import Cursor
from typing import Optional
from urllib import response
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# Define Data object (like java object) using pydantic BaseModel
class Post(BaseModel):
    title: str
    content: str
    # Adding Default Value to the Field
    published: bool = True
    # Adding Optional Field with default value None
    rating: Optional[int] = None 

# It is important that we connect to the database before we start the server
try:
    # Connect to your postgres DB
    conn = psycopg2.connect(host = 'localhost', 
                            database = 'fastapi', 
                            user = 'postgres', 
                            password = 'toor',
                            cursor_factory = RealDictCursor)
    
    # Open a cursor to perform database operations
    cursor = conn.cursor()
    print("Database Connection was Successful")
    
except:
    print('Failed to Connect to Database')
    print('Error: ', Exception)

# Defining Posts
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favoirite food", "content": "pizza", "id": 2}]

# @: Function decorater to perform get request (hence @app.get)
# to the root of the server (hence "/")
# The parameter can be changes to whichever subaddress, like "/user/login"
# and the user will have to perform GET request to that address, i.e., 
# <server_address> +  "user/login"

# Use command uvicorn main:app --reload to start the server
# --reload to enable hot reloading

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
async def get_posts():
    # Execute a query
    cursor.execute(""" SELECT * FROM POSTS """)
    # Use fetchall or fetchone or fetchany to return query results
    buff = cursor.fetchall()
    return {"data": buff}


# Here the {id} is a path parameter
# It can directly be retrieved by the decorating function
# "id: int": Explicit type check and type casting for {id}
# parameter to integer datatype
@app.get("/posts/{id}")
# async def get_post_by_id(id: int, response: Response):
async def get_post_by_id(id: int):
    cursor.execute(""" SELECT * FROM POSTS WHERE id = %s""", (str(id)))
    buff = cursor.fetchone()
    # If post does not exist raise exception
    if buff is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="post does not exist")
    return buff
    


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(new_post: Post):
    print(new_post)
    # return new_post
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
                    # cursor.execute takes the sql and a tuple of params
                    (new_post.title, new_post.content, new_post.published)
                    )
    # buff = cursor.fetchall()
    buff = cursor.fetchone()
    # Commit the changes to the DB
    conn.commit()
    return buff


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_by_id(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    buff = cursor.fetchone()
    # If post does not exist raise exception
    if buff is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="post does not exist")
    conn.commit()
    
    # We cannot return data if we are using status code 204
    # Hence we return the response as status code 204
    # When we use status code 204, no data is returned
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
async def update_post_by_id(id: int, updated_post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                    (updated_post.title, updated_post.content, updated_post.published, str(id)))
    buff = cursor.fetchone()
    
    if buff is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="post does not exist")
    
    
    conn.commit()
    return buff