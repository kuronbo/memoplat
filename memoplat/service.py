"""
service.py
----------
このモジュールは、外界との接点である。
外のプログラムはこのモジュールにある関数を用いて、memoplatというプログラムを
操作することになる。

基本的には、crudという種類の関数しかなく、
結果は`Response`というdictライクなクラスが返される。

また、metplatは2つのレポジトリでドメインの永続化を管理しており、
このモジュールには、`memo_repo`, `category_repo`という2つの
レポジトリのインスタンスが設定されている。
"""
from memoplat.persistence.impl.impl_sqlalchemy import repository

from memoplat.exceptions import MemoPlatError


memo_repo = repository.AlcMemoRepository()
category_repo = repository.AlcCategoryRepository()


def wrap_error_decorator(func):
    def wrapper(*args):
        try:
            return func(*args)
        except Exception:
            raise MemoPlatError
    return wrapper


##############################################################################
# command ####################################################################
##############################################################################
def create_memo(category_name, title, caption, tagnames):
    category = category_repo.get(category_name, by='name')
    if not category:
        raise Exception
    memo = memo_repo.new(category_id='c1', title=title, caption=caption,
                         tagnames=tagnames)
    memo_repo.save(memo)
    memo_repo.commit()


def remove_memo(id):
    memo_repo.remove(id)
    memo_repo.commit()


def create_category(name):
    category = category_repo.new(name=name)
    category_repo.save(category)
    category_repo.commit()


##############################################################################
# query ######################################################################
##############################################################################

# memo


if __name__ == '__main__':
    create_memo(category_name='簡単読書', title='title', caption='caption', tagnames=['tag1', 'tag2'])


