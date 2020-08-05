from sqlalchemy import create_engine   
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
import os

import config

POSTGRES_DATABASE_URL = None

if config.ENV_DEV:
	from local_config import POSTGRES_URL
	POSTGRES_DATABASE_URL = POSTGRES_URL
else:
	POSTGRES_DATABASE_URL = os.environ.get('DATABASE_URL')

db_engine = create_engine(POSTGRES_DATABASE_URL)

Session = sessionmaker(db_engine)
base = declarative_base()
