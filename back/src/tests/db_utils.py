import os
import sqlalchemy
from sqlalchemy.exc import ProgrammingError, OperationalError
from app.db.models import metadata
from app.config import settings
import logging

# logging.basicConfig(level=logging.INFO)


def create_fake_db():
    engine = sqlalchemy.create_engine(db_url())
    with engine.connect() as conn:
        drop_db(conn)
        create_db(conn)

    engine = sqlalchemy.create_engine(settings.DATABASE_URL)
    metadata.create_all(engine)

def db_url():
    return f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{os.getenv('POSTGRES_DB')}"    

def drop_db(conn):
    try:
        conn = conn.execution_options(autocommit=False)
        conn.execute('ROLLBACK')
        conn.execute(f'DROP DATABASE {settings.DB_NAME}')
    except ProgrammingError:
        logging.info('Could not drop the database, probably does not exist.')
        conn.execute('ROLLBACK')
    except OperationalError:
        logging.info('Could not drop database because it’s being accessed by other users (psql prompt open?)')
        conn.execute('ROLLBACK')      
    logging.info(f'{settings.DB_NAME} db dropped!')        
        
def create_db(conn):
    conn.execute(f'CREATE DATABASE {settings.DB_NAME}')
    try:
        conn.execute(f"create user {settings.DB_USER} with encrypted password '{settings.DB_PASSWORD}'")
    except:
        logging.info('User already exists.')
        conn.execute(f'grant all privileges on database {settings.DB_NAME} to {settings.DB_USER}')

        
 