from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(Text)
    published = Column(TIMESTAMP)

    def __init__(self, title, body, published):
        self.title = title
        self.body = body
        self.published = published
