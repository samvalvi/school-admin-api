import databases as databases
from dotenv import load_dotenv
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv(getenv('ENV_FILE'))

engine = create_engine(getenv('DATABASE_URL'), pool_size=15, max_overflow=20)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency Injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
