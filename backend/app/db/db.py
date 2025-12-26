from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from config.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
session = sessionmaker(autoflush=False,autocommit=False,bind=engine)
base = declarative_base()
