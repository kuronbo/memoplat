from itertools import groupby

from sqlalchemy import desc, asc

from memoplat.persistence.impl.impl_sqlalchemy import db
from memoplat.persistence.impl.impl_sqlalchemy.config import generate_session


class Query:
    def __init__(self, offset=0, limit=10, order_by='id', desc_asc='desc'):
        self.offset = offset
        self.limit = limit
        self.order_by = order_by
        self.desc_asc = desc_asc


class MemoQuery(Query):
    """TODO:like文においてupperとlowerが区別されていない。sqliteの仕様か？"""
    def some(self):
        return self._generate_responses({})

    def some_like(self, req):
        filters = []
        for k, v in req:
            filters.append(db.Memo.__dict__[k].like('%{}%'.format(v)))
        return self._generate_responses(filters)

    def some_eq(self, req):
        filters = []
        for k, v in req:
            filters.append(db.Memo.__dict__[k]==v)
        return self._generate_responses(filters)

    def some_eq_tagname(self, tagname):
        session = generate_session()
        memo_ids = [r[0] for r in session.query(db.Tag.memo_id).filter_by(name=tagname).all()]
        filters = [db.Memo.id.in_(memo_ids)]
        return self._generate_responses(filters, session=session)

    def some_eq_like(self, eq_req, like_req):
        filters = []
        for k, v in eq_req:
            filters.append(db.Memo.__dict__[k]==v)
        for k, v in like_req:
            filters.append(db.Memo.__dict__[k].like('%{}%'.format(v)))
        return self._generate_responses(filters)

    def _prepare_query(self, session):
        """TODO:outerjoinよりjoinじゃね？"""
        return session.query(db.Memo, db.Tag).\
            outerjoin(db.Tag, db.Memo.id==db.Tag.memo_id)

    def _complete_query(self, q):
        if self.desc_asc == 'desc':
            q = q.order_by(desc(db.Memo.__dict__[self.order_by]))
        else:
            q = q.order_by(asc(db.Memo.__dict__[self.order_by]))
        return q.limit(self.limit).offset(self.offset)

    def _generate_responses(self, filters, session=None):
        session = generate_session() if not session else session
        q = self._prepare_query(session)
        q = q.filter(*filters) if filters else q
        q = self._complete_query(q)

        responses = []
        group = groupby(q.all(), key=lambda x: x[0])
        for k, g in group:
            tagnames = [t.name for _, t in g if t]
            memo = k
            response = {'id': memo.id,
                        'category_id': memo.category_id,
                        'title': memo.title,
                        'caption': memo.caption,
                        'tagnames': tagnames,
                        'created_at': memo.created_at.strftime('%Y-%m-%d %H:%M:%S')}
            responses.append(response)
        return responses


class TagQuery(Query):
    def some_like(self, req):
        filters = []
        for k, v in req:
            filters.append(db.Tag.__dict__[k].like('%{}%'.format(v)))
        return self._generate_names(filters)

    def _generate_names(self, filters):
        session = generate_session()
        q = session.query(db.Tag.name).group_by(db.Tag.name).filter(*filters)
        q = self._complete_query(q)
        return [r[0] for r in q.all()]

    def _complete_query(self, q):
        if self.desc_asc == 'desc':
            q = q.order_by(desc(db.Tag.__dict__[self.order_by]))
        else:
            q = q.order_by(asc(db.Tag.__dict__[self.order_by]))
        return q.limit(self.limit).offset(self.offset)
