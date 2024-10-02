
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.utils.get_envs import envs

DATABASE_URL = envs()['DATBASE_SQL_URL']
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker( autocommit=False, autoflush=False, bind=engine )
Base = declarative_base()