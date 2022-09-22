from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# THe url used too connect to the engine
# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:toor@localhost/fastapi"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# Engine connection to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Creates a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for defining table objects
Base  = declarative_base()

# Function to connect to the database, performt the requested operaiton
# and then close the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()