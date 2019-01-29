"""
DB設計のイメージ

tables:
    memo: メモ
    tag: タグ

relationship:
    one to many : memo と tag

TODO: memoとtagのcascadeを考える。
"""
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Memo(Base):
    __tablename__ = 'memo'

    id = Column(String, primary_key=True)
    category_id = Column(String)
    title = Column(String)
    caption = Column(String)
    tags = relationship('Tag', cascade="delete, save-update, merge, delete-orphan")
    created_at = Column(DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'title': self.title,
            'caption': self.caption,
            'tags': self.tags,
            'created_at': self.created_at
        }


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(String, primary_key=True)
    name = Column(String)
    memo_id = Column(String, ForeignKey('memo.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }
