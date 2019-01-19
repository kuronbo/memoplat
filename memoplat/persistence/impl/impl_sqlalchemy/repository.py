from memoplat.domain import models
from memoplat.persistence.interface import MemoRepository, CategoryRepository, \
    TagRepository
from memoplat.persistence.impl.impl_sqlalchemy import db


class PersistenceMixin:
    def flush(self):
        self.session.flush()

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()


class AlcMemoRepository(PersistenceMixin, MemoRepository):
    def __init__(self):
        self.session = db.Session()

    def save(self, memo, update=False):
        if not update:
            self.session.add(db.Memo(id=memo.id, category_id=memo.category_id,
                                     title=memo.title, caption=memo.caption,
                                     created_at=memo.created_at))
        self.flush()


class AlcCategoryRepository(PersistenceMixin, CategoryRepository):
    def __init__(self):
        self.session = db.Session()

    def save(self, category):
        self.session.add(db.Category(id=category.id, name=category.name))
        self.flush()

    def get(self, value, by='id'):
        c = self.session.query(db.Category).\
            filter(db.Category.__dict__[by]==value).first()
        return models.Category(*c.to_dict()) if c else None


class AlcTagRepository(PersistenceMixin, TagRepository):
    def __init__(self):
        self.session = db.Session()

    def save_some(self, tags, memo_id):
        self.session.query(db.Tag).filter_by(memo_id=memo_id).delete()
        self.session.add_all([db.Tag(id=tag.id, name=tag.name, memo_id=memo_id)
                              for tag in tags])
        self.flush()

    def get_tags(self, values, by='id'):
        result = self.session.query(db.Tag).\
            filter(db.Tag.__dict__[by].in_(values)).all()
        if result:
            return [models.Tag(*v) for v in result]
        else:
            return []
