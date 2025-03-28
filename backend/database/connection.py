from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database configuration
DATABASE_URL = "postgresql://dialuser:Hello123%23@dial-ai.cdu0ckg00b4n.us-west-2.rds.amazonaws.com:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database connection utility
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 