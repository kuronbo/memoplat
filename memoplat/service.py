"""
service.py
----------
このモジュールは、外界との接点である。
外のプログラムはこのモジュールにある関数を用いて、memoplatというプログラムを
操作することになる。

基本的には、crudという種類の関数しかなく、
結果は`Response`というdictライクなクラスが返される。

また、metplatは3つのレポジトリでドメインの永続化を管理しており、
このモジュールには、`memo_repo`, `tag_repo`, `category_repo`という3つの
レポジトリのインスタンスが設定されている。
"""
from memoplat.domain.models import Memo, Category, Tag
from memoplat.persistence.impl.impl_sqlalchemy import repository

from memoplat.exceptions import MemoPlatError


memo_repo = repository.AlcMemoRepository()
tag_repo = repository.AlcTagRepository()
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
#@wrap_error_decorator
def create_memo(category_name, title, caption, tagnames):
    category = category_repo.get(category_name, by='name')
    if not category:
        raise Exception
    tags = tag_repo.get_tags(tagnames, by='name')
    memo = Memo.new_instance(category.id, title, caption,
                             tag_ids=[tag.id for tag in tags])
    tag_repo.save_some(tags, memo.id)
    memo_repo.save(memo)
    tag_repo.commit()
    memo_repo.commit()



@wrap_error_decorator
def remove_memo(id):
    memo_repo.remove(id)
    memo_repo.commit()


##############################################################################
# query ######################################################################
##############################################################################



if __name__ == '__main__':
    create_memo('aiueo', 'title', 'cap', ['tag1', 'tag2'])
