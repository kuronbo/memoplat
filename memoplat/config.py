from memoplat.persistence.impl.impl_sqlalchemy import repository
from memoplat.persistence.impl.impl_sqlalchemy.config import create_table, \
    set_db_engine


MEMO_REPO = None
CATEGORY_REPO = None


def configure(sqlite_path):
    global MEMO_REPO
    global CATEGORY_REPO

    set_db_engine(sqlite_path)
    create_table()
    MEMO_REPO = repository.AlcMemoRepository()
    CATEGORY_REPO = repository.AlcCategoryRepository()
