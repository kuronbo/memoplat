"""
DB設計のイメージ

tables:
    memo: メモ
    category: カテゴリ
    tag: タグ

relationship:
    one to many : memo と tag
    many to one : memo と category

TODO: memoとtagのcascadeを考える。
"""
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


DB_ENGINE = create_engine('sqlite:///persistence/impl/impl_sqlalchemy/sqlite.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=DB_ENGINE)


class Memo(Base):
    __tablename__ = 'memo'

    id = Column(String, primary_key=True)
    category_id = Column(String, ForeignKey('category.id'))
    category = relationship('Category', backref='memos')
    title = Column(String)
    caption = Column(String)
    tags = relationship('Tag', cascade="delete, save-update, merge, delete-orphan")
    created_at = Column(DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'category_id': self.category.id,
            'title': self.title,
            'caption': self.caption,
            'tags': self.tags,
            'created_at': self.created_at
        }


class Category(Base):
    __tablename__ = 'category'

    id = Column(String, primary_key=True)
    name = Column(String)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
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


if __name__ == '__main__':
    Base.metadata.drop_all(bind=DB_ENGINE)
    Base.metadata.create_all(bind=DB_ENGINE)
