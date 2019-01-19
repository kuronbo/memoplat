from itertools import groupby

from sqlalchemy import desc, asc

from memoplat.persistence.impl.impl_sqlalchemy import db


class Query:
    def __init__(self, offset, limit, order_by, desc_asc):
        self.offset = offset
        self.limit = limit
        self.order_by = order_by
        self.desc_asc = desc_asc


class MemoQuery(Query):
    """TODO:like文においてupperとlowerが区別されていない。sqliteの仕様か？"""
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

    def some_eq_like(self, eq_req, like_req):
        filters = []
        for k, v in eq_req:
            filters.append(db.Memo.__dict__[k]==v)
        for k, v in like_req:
            filters.append(db.Memo.__dict__[k].like('%{}%'.format(v)))
        return self._generate_responses(filters)

    def _prepare_query(self, session):
        """TODO:outerjoinよりjoinじゃね？"""
        return session.query(db.Memo, db.Category, db.Tag).\
            outerjoin(db.Category, db.Memo.category_id==db.Category.id).\
            outerjoin(db.Tag, db.Memo.id==db.Tag.memo_id)

    def _complete_query(self, q):
        if self.desc_asc == 'desc':
            q = q.order_by(desc(db.Memo.__dict__[self.order_by]))
        else:
            q = q.order_by(asc(db.Memo.__dict__[self.order_by]))
        return q.limit(self.limit).offset(self.offset)

    def _generate_responses(self, filters):
        session = db.Session()
        q = self._prepare_query(session)
        q = q.filter(*filters)
        q = self._complete_query(q)

        responses = []
        group = groupby(q.all(), key=lambda x: (x[0], x[1]))
        for k, g in group:
            tagnames = [t.name for _, _, t in g if t]
            category_name = k[1].name if k[1] else None
            memo = k[0]
            response = {'id': memo.id,
                        'category_name': category_name,
                        'title': memo.title,
                        'caption': memo.caption,
                        'tagnames': tagnames,
                        'created_at': memo.created_at.strftime('%Y-%m-%d $H:%M:%S')}
            responses.append(response)
        return responses


class TagQuery(Query):
    def some_like(self, req):
        filters = []
        for k, v in req:
            filters.append(db.Tag.__dict__[k].like('%{}%'.format(v)))
        return self._generate_names(filters)

    def _generate_names(self, filters):
        session = db.Session()
        q = session.query(db.Tag.name).filter(*filters)
        q = self._complete_query(q)
        return {r[0] for r in q.all()}

    def _complete_query(self, q):
        if self.desc_asc == 'desc':
            q = q.order_by(desc(db.Tag.__dict__[self.order_by]))
        else:
            q = q.order_by(asc(db.Tag.__dict__[self.order_by]))
        return q.limit(self.limit).offset(self.offset)
