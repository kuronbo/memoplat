"""
service.py
----------
このモジュールは、外界との接点である。
外のプログラムはこのモジュールにある関数を用いて、memoplatというプログラムを
操作することになる。

基本的には、crudという種類の関数しかなく、
readの結果は、pythonのプリミティブ型で返される。

また、metplatは2つのレポジトリでドメインの永続化を管理しており、
このモジュールには、`memo_repo`, `category_repo`という2つの
レポジトリのインスタンスが設定されている。
"""
from memoplat.persistence.impl.impl_sqlalchemy import querys
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
# create delete ##############################################################
##############################################################################
@wrap_error_decorator
def create_memo(category_name, title, caption, tagnames):
    category = category_repo.get(category_name, by='name')
    if not category:
        raise Exception
    memo = memo_repo.new(category_id=category_name, title=title, caption=caption,
                         tagnames=tagnames)
    memo_repo.save(memo)
    memo_repo.commit()


@wrap_error_decorator
def delete_memo(id):
    memo_repo.remove(id)
    memo_repo.commit()


@wrap_error_decorator
def create_category(name):
    category = category_repo.new(name=name)
    category_repo.save(category)
    category_repo.commit()


##############################################################################
# query ######################################################################
##############################################################################

# memo
@wrap_error_decorator
def read_one_memo_eq_id(id):
    query = querys.MemoQuery()
    result = query.some_eq([('id', id)])
    return result[0] if result else []


@wrap_error_decorator
def read_some_memo_eq_tagname(tagname, page=0, page_size=10, desc_asc='desc'):
    query = querys.MemoQuery(offset=page*page_size, limit=page_size,
                             order_by='created_at', desc_asc=desc_asc)
    result = query.some_eq_tagname(tagname)
    return result


@wrap_error_decorator
def read_some_memo_eq_categoryid(category_id, page=0, page_size=10, desc_asc='desc'):
    query = querys.MemoQuery(offset=page*page_size, limit=page_size,
                             order_by='created_at', desc_asc=desc_asc)
    result = query.some_eq([('category_id', category_id)])
    return result


@wrap_error_decorator
def read_some_memo_like_title(value, page=0, page_size=10, desc_asc='desc'):
    query = querys.MemoQuery(offset=page*page_size, limit=page_size,
                             order_by='created_at', desc_asc=desc_asc)
    req = [('title', value)]
    result = query.some_like(req)
    return result


@wrap_error_decorator
def read_some_memo_like_caption(value, page=0, page_size=10, desc_asc='desc'):
    query = querys.MemoQuery(offset=page*page_size, limit=page_size,
                             order_by='created_at', desc_asc=desc_asc)
    req = [('caption', value)]
    result = query.some_like(req)
    return result


# tag
@wrap_error_decorator
def read_some_tag_like_name(value, page=0, page_size=10, desc_asc='desc'):
    query = querys.TagQuery(offset=page*page_size, limit=page_size,
                            order_by='name', desc_asc=desc_asc)
    req = [('name', value)]
    result = query.some_like(req)
    return result


if __name__ == '__main__':
    create_category('name')
