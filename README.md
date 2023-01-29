# FASTAPI + Postgresql
A sample Fastapi plus Postgresql backend for social media platform like twitter.
It performs CRUD operations on users and posts and OAuth2 based authentication
Tech stack includes:
 - Python
 - PostgreSQL
 - FastAPI
 - SQLAlchemy ORM
 - Alembic for Database Migration

## Setup
To setup, run the following commands in the main directory:
```
python -m venv venv
./venv/Scripts/Activate.psi
pip install -r requirements.txt
```

To start the webserver run the following command:
```
uvicorn app.main:app --reload
```

For documentation start the webserver and then open ```localhost:8000/docs``` in a web-browser
