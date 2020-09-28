from sqlalchemy import create_engine   
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
import os

import config

# Configure the PosgreSQL database url
POSTGRES_DATABASE_URL = None

if config.ENV_LOCAL_DEV:
	# If developing locally, should be one set in local_config.py
	from local_config import POSTGRES_URL
	POSTGRES_DATABASE_URL = POSTGRES_URL
else:
	# If remote, should be an environment variable on Heroku
	POSTGRES_DATABASE_URL = os.environ.get('DATABASE_URL')

if not POSTGRES_DATABASE_URL:
	raise Exception(
		"Could not find a valid PostgreSQL database url. "
		"If hosting locally, check the config file, then check the url of local_config file. "
		"If hosting remotely, check settings on deployment platform. "
	)

# Run and create the engine, session, and base
print('running postgres database on %s' % POSTGRES_DATABASE_URL)
db_engine = create_engine(POSTGRES_DATABASE_URL)
Session = sessionmaker(db_engine)
base = declarative_base()
