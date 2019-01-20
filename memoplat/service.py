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
from memoplat.exceptions import MemoPlatError
from memoplat import config


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
    category = config.CATEGORY_REPO_MEMOPLAT.get(category_name, by='name')
    if not category:
        raise Exception
    memo = config.MEMO_REPO_MEMOPLAT.new(category_id=category_name, title=title, caption=caption,
                                         tagnames=tagnames)
    config.MEMO_REPO_MEMOPLAT.save(memo)
    config.MEMO_REPO_MEMOPLAT.commit()


@wrap_error_decorator
def delete_memo(id):
    config.MEMO_REPO_MEMOPLAT.remove(id)
    config.MEMO_REPO_MEMOPLAT.commit()


@wrap_error_decorator
def create_category(name):
    category = config.CATEGORY_REPO_MEMOPLAT.new(name=name)
    config.CATEGORY_REPO_MEMOPLAT.save(category)
    config.CATEGORY_REPO_MEMOPLAT.commit()


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
