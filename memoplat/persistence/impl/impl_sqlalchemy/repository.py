from memoplat.domain import models
from memoplat.persistence.interface import MemoRepository
from memoplat.persistence.impl.impl_sqlalchemy import db
from memoplat.persistence.impl.impl_sqlalchemy.config import generate_session

class PersistenceMixin:
    def flush(self):
        self.session.flush()

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()


class AlcMemoRepository(PersistenceMixin, MemoRepository):
    def __init__(self):
        self.session = None

    def new(self, **kwargs):
        return models.Memo.new_instance(
            id=kwargs['id'],
            category_id=kwargs['category_id'],
            title=kwargs['title'],
            caption=kwargs['caption'],
            tagnames=kwargs['tagnames'])

    def save(self, memo, update=False):
        self.session = generate_session()
        if not update:
            m = db.Memo(id=memo.id, category_id=memo.category_id,
                        title=memo.title, caption=memo.caption,
                        created_at=memo.created_at)
            m.tags = [db.Tag(id=memo.id+str(i), name=name)
                      for i, name in enumerate(memo.tagnames)]
            self.session.add(m)
        else:
            m = self.session.query(db.Memo).filter_by(id=memo.id).first()
            m.id = memo.id
            m.title = memo.title
            m.caption = memo.caption
            m.tags = [db.Tag(id=memo.id+str(i), name=name)
                          for i, name in enumerate(memo.tagnames)]
        self.flush()

    def remove(self, value, by='id'):
        self.session = generate_session()
        if by not in ['id', 'category_id']:
            raise ValueError('`by`の値は"id"or"category_id"のみです。')
        self.session.query(db.Memo).\
            filter(db.Memo.__dict__[by]==value).\
            delete()
        self.flush()
