from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

conf_filepath = 'config/db_conf.json'

def read_config(file_path):
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    return config

config = read_config(conf_filepath)

database_config = config['database']
host = database_config['host']
dbname = database_config['dbname']
user = database_config['user']
password = database_config['password']

# https://stackoverflow.com/questions/73596058/creating-an-sqlalchemy-engine-based-on-psycopg3
# To use psycopg3, connection string should be in the format: postgresql+psycopg...
SQLALCHEMY_DB_URL = f"postgresql+psycopg://{user}:{password}@{host}/{dbname}"

engine = create_engine(SQLALCHEMY_DB_URL)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
