from sqlalchemy import create_engine   
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker

from config import POSTGRES_URL

POSTGRES_DATABASE_URL = POSTGRES_URL

db_engine = create_engine(POSTGRES_DATABASE_URL)

Session = sessionmaker(db_engine)
base = declarative_base()
