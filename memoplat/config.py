from memoplat.persistence.impl.impl_sqlalchemy import repository
from memoplat.persistence.impl.impl_sqlalchemy.config import create_table, \
    set_db_engine


MEMO_REPO_MEMOPLAT = None
CATEGORY_REPO_MEMOPLAT = None


def configure(sqlite_path):
    global MEMO_REPO_MEMOPLAT
    global CATEGORY_REPO_MEMOPLAT

    set_db_engine(sqlite_path)
    create_table()
    MEMO_REPO_MEMOPLAT = repository.AlcMemoRepository()
    CATEGORY_REPO_MEMOPLAT = repository.AlcCategoryRepository()
