from fastapi import FastAPI
# import psycopg2
# from psycopg2.extras import RealDictCursor
from . import models
from .database import engine
from .utils import *
from .routers import post, user, auth, vote
from .config import settings

from fastapi.middleware.cors import CORSMiddleware

# Migration command to create table in case if it does not exist
# Not needed if you are using alembic
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# List of domains that can send requests to your APIs
# "*" means all sites are allowed (wildcard)
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    # Limit http methods (PUT, POST, DELETE, etc) coming to your backend
    allow_methods=["*"],
    allow_headers=["*"],
)

'''
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
'''

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


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)