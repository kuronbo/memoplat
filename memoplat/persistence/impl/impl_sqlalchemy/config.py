from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from memoplat.persistence.impl.impl_sqlalchemy.db import Base


DB_ENGINE = create_engine('sqlite:///:memory:')


def generate_session():
    return Session(bind=DB_ENGINE)


def create_table():
    Base.metadata.create_all(bind=DB_ENGINE)


def set_db_engine(sqlite_path):
    global DB_ENGINE
    DB_ENGINE = create_engine('sqlite:///{}'.format(sqlite_path))
