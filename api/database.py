from sqlalchemy import create_engine

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from api.settings import settings

DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
