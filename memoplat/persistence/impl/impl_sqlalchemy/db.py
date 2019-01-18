"""
DB設計のイメージ

tables:
    memo: メモ
    category: カテゴリ
    tag: タグ
    memo_tag_table: メモとタグのidテーブル

relationship:
    memo-category: many to one
    memo-tag: many to many (memo_tag_tableを間に噛ませてる)
"""
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


engine = create_engine('sqlite:///test.sqlite.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

memo_tag_table = Table('memo_tag', Base.metadata,
                       Column('memo_id', String, ForeignKey('memo.id')),
                       Column('tag_id', String, ForeignKey('tag.id')))


class Memo(Base):
    __tablename__ = 'memo'

    id = Column(String, primary_key=True)
    category_id = Column(String, ForeignKey('category.id'))
    category = relationship('Category', backref='memos')
    title = Column(String)
    caption = Column(String)
    tags = relationship('Tag', secondary=memo_tag_table,
                        back_populates='memos')
    created_at = Column(DateTime)


class Category(Base):
    __tablename__ = 'category'

    id = Column(String, primary_key=True)
    name = Column(String)


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(String, primary_key=True)
    name = Column(String)
    memos = relationship('Memo', secondary=memo_tag_table,
                         back_populates='tags')


if __name__ == '__main__':
    from datetime import datetime

    session = Session()

    print(session.query(Category).all()[0].memos[0].tags)
