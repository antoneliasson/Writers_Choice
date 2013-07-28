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

from sqlalchemy.sql import func

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'
    __table_args__ = {
        'mysql_engine' : 'InnoDB',
        'mysql_charset' : 'utf8'
    }
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    _body = Column('body', Text, nullable=False)
    published = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())

    def __init__(self, title, body, published):
        self.title = title
        self._body = '\n'.join(body.splitlines())
        self.published = published

    def get_body(self):
        return self._body
    def set_body(self, value):
        self._body = '\n'.join(value.splitlines())
    def del_body(self):
        del self._body
    body = property(get_body, set_body, del_body)

class RootFactory():
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, 'group:editors', 'edit') ]
    def __init__(self, request):
        pass
