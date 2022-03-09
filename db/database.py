"""
Connects to Database
"""
# pylint: disable=import-error
# pylint: disable=invalid-name

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


load_dotenv()
#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = os.environ.get("postgres_uri")

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL
# )
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Connects to database
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
