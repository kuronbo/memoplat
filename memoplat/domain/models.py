from datetime import datetime
from uuid import uuid4


class Memo:
    """メモ

    Attributes:
        id (str): 固有id
        category_id (str): カテゴリ(:class:`Category`)のid
        title (str): タイトル
        caption (str): 簡単な説明文
        tagnames (list(str)): タグの名前のリスト
        created_at (datetime.datetime): 作成された日時
    """
    def __init__(self, id, category_id, title, caption, tagnames, created_at):
        self.id = id
        self.category_id = category_id
        self.title = title
        self.caption = caption
        self.tagnames = list(set(tagnames)) if tagnames else []
        self.created_at = created_at

    @classmethod
    def new_instance(cls, category_id, title, caption, tagnames):
        id = str(uuid4())[:8]
        created_at = datetime.now()
        return cls(id, category_id, title, caption, tagnames, created_at)

    def __repr__(self):
        cls = type(self)
        return '<{cls.__name__}(id={self.id!r}, category_id={self.category_id!r},' \
               ' title={self.title!r}, caption={self.caption!r}, ' \
               'created_at={self.created_at!r})>'.format(cls=cls, self=self)


class Category:
    """カテゴリ

    Attributes:
        id (str): 固有id
        name (str): 名前
    """
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def new_instance(cls, name):
        id = str(uuid4())[:8]
        return cls(id, name)

    def __repr__(self):
        cls = type(self)
        return '<{cls.__name__}(id={self.id!r}, name={self.name!r})>'\
            .format(cls=cls, self=self)
