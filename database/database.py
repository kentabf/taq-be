from sqlalchemy import create_engine   
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
import os

import config

POSTGRES_DATABASE_URL = None

if config.ENV_LOCAL_DEV:
	from local_config import POSTGRES_URL
	POSTGRES_DATABASE_URL = POSTGRES_URL
	print("this this this1")
else:
	POSTGRES_DATABASE_URL = os.environ.get('DATABASE_URL')

print("this this this")
print(POSTGRES_DATABASE_URL)
db_engine = create_engine(POSTGRES_DATABASE_URL)

Session = sessionmaker(db_engine)
base = declarative_base()
