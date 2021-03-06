"""
service.py
----------
このモジュールは、外界との接点である。
外のプログラムはこのモジュールにある関数を用いて、memoplatというプログラムを
操作することになる。

基本的には、crudという種類の関数しかなく、
readの結果は、pythonのプリミティブ型で返される。

また、metplatは1つのレポジトリでドメインの永続化を管理している。
そのレポジトリはconfigモジュールに`MEMO_REPO_MEMOPLAT`として設定されている。
"""
from memoplat.persistence.impl.impl_sqlalchemy import querys
from memoplat import config


##############################################################################
# create delete ##############################################################
##############################################################################
class create_memo:
    def __init__(self, id, category_id, title, caption, tagnames):
        self.id = id
        self.category_id = category_id
        self.title = title
        self.caption = caption
        self.tagnames = tagnames

        self.flushed = False

    def flush(self):
        memo = config.MEMO_REPO_MEMOPLAT.new(id=self.id,
                                             category_id=self.category_id,
                                             title=self.title,
                                             caption=self.caption,
                                             tagnames=self.tagnames)
        config.MEMO_REPO_MEMOPLAT.save(memo)
        self.flushed = True

    def commit(self):
        config.MEMO_REPO_MEMOPLAT.commit()


class delete_memo:
    def __init__(self, id):
        self.id = id

        self.flushed = False

    def flush(self):
        config.MEMO_REPO_MEMOPLAT.remove(id)

    def commit(self):
        config.MEMO_REPO_MEMOPLAT.commit()


##############################################################################
# query ######################################################################
##############################################################################

# memo
def read_one_memo_eq_id(id):
    query = querys.MemoQuery()
    result = query.some_eq([('id', id)])
    return result[0] if result else []


def read_some_memo(page=0, page_size=10, desc_asc='desc'):
    query = querys.MemoQuery(offset=page*page_size, limit=page_size,
                             order_by='created_at', desc_asc=desc_asc)
    result = query.some()
    return result


def read_some_memo_eq_tagname(tagname, page=0, page_size=10, desc_asc='desc'):
    query = querys.MemoQuery(offset=page*page_size, limit=page_size,
                             order_by='created_at', desc_asc=desc_asc)
    result = query.some_eq_tagname(tagname)
    return result


def read_some_memo_eq_categoryid(category_id, page=0, page_size=10, desc_asc='desc'):
    query = querys.MemoQuery(offset=page*page_size, limit=page_size,
                             order_by='created_at', desc_asc=desc_asc)
    result = query.some_eq([('category_id', category_id)])
    return result


def read_some_memo_like_title(value, page=0, page_size=10, desc_asc='desc'):
    query = querys.MemoQuery(offset=page*page_size, limit=page_size,
                             order_by='created_at', desc_asc=desc_asc)
    req = [('title', value)]
    result = query.some_like(req)
    return result


def read_some_memo_like_caption(value, page=0, page_size=10, desc_asc='desc'):
    query = querys.MemoQuery(offset=page*page_size, limit=page_size,
                             order_by='created_at', desc_asc=desc_asc)
    req = [('caption', value)]
    result = query.some_like(req)
    return result


# tag
def read_some_tag_like_name(value, page=0, page_size=10, desc_asc='desc'):
    query = querys.TagQuery(offset=page*page_size, limit=page_size,
                            order_by='name', desc_asc=desc_asc)
    req = [('name', value)]
    result = query.some_like(req)
    return result


if __name__ == '__main__':
    from memoplat import config

    config.configure(':memory:')
    com = create_memo('1', 'm_covers', 'title', 'caption', ['tag1', 'tag2'])
    com.flush()
    com.commit()
    print(read_some_memo_like_title('tit'))