from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from memoplat.persistence.impl.impl_sqlalchemy.db import Base


DB_ENGINE_MEMOPLAT = create_engine('sqlite:///:memory:')


def generate_session():
    return Session(bind=DB_ENGINE_MEMOPLAT)


def create_table():
    Base.metadata.create_all(bind=DB_ENGINE_MEMOPLAT)


def set_db_engine(sqlite_path):
    global DB_ENGINE_MEMOPLAT
    DB_ENGINE_MEMOPLAT = create_engine('sqlite:///{}?check_same_thread=False'.format(sqlite_path))
