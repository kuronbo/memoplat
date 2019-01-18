from memoplat.persistence.interface import MemoRepository, CategoryRepository, \
    TagRepository
from memoplat.persistence.impl.impl_sqlalchemy import db


class AlcMemoRepository(MemoRepository):
    def save(self, memo):
        session = db.Session()
        m = db.Memo(id=memo.id, title=memo.title, caption=memo.caption,
                    created_at=memo.created_at)
        m.category = db.Category()
