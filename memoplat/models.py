class Memo:
    """メモ

    Attributes:
        id_ (str): 固有id
        category_id (str): カテゴリ(:class:`Category`)のid
        title (str): タイトル
        caption (str): 簡単な説明文
        tag_ids (list(str)): タグ(:class:`Tag`)のidリスト
        created_at (datetime.datetime): 作成された日時
    """
    def __init__(self, id_, category_id, title, caption, tag_ids, created_at):
        self.id = id_
        self.category_id = category_id
        self.title = title
        self.caption = caption
        self.tag_ids = list(tag_ids) if tag_ids else []
        self.created_at = created_at

    def __repr__(self):
        cls = type(self)
        return '{cls.__name__}(id_={self.id!r}, category_id={self.category_id!r},' \
               ' title={self.title!r}, caption={self.caption!r}, ' \
               'created_at={self.created_at!r})'.format(cls=cls, self=self)


class Category:
    """カテゴリ

    Attributes:
        id_ (str): 固有id
        name (str): 名前
    """
    def __init__(self, id_, name):
        self.id = id_
        self.name = name

    def __repr__(self):
        cls = type(self)
        return '{cls.__name__}(id_={self.id!r}, name={self.name!r})'\
            .format(cls=cls, self=self)


class Tag:
    """タグ

    Attributes:
        id_ (str): 固有id
        name (str): 名前
    """
    def __init__(self, id_, name):
        self.id = id_
        self.name = name

    def __repr__(self):
        cls = type(self)
        return '{cls.__name__}(id_={self.id!r}, name={self.name!r})' \
            .format(cls=cls, self=self)
