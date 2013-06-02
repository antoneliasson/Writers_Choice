from pyramid.security import (
    Allow,
    Everyone,
    )

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
    __table_args__ = {'mysql_engine':'InnoDB'}
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    published = Column(TIMESTAMP, nullable=False)

    def __init__(self, title, body, published):
        self.title = title
        self.body = body
        self.published = published

class RootFactory():
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, 'group:editors', 'edit') ]
    def __init__(self, request):
        pass
