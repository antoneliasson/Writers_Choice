from datetime import datetime

from markdown.extensions import headerid

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
    Boolean,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from sqlalchemy.sql import expression

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

def make_slug(string):
    return headerid.slugify(string, '-')

class WrittenContent(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    _body = Column('body', Text, nullable=False)
    slug = Column(String(255), nullable=False)

    def __init__(self, title, body):
        self.title = title
        self._body = '\n'.join(body.splitlines())
        self.slug = make_slug(self.title)

    def get_body(self):
        return self._body
    def set_body(self, value):
        self._body = '\n'.join(value.splitlines())
    body = property(get_body, set_body)

class Article(WrittenContent):
    __tablename__ = 'articles'

    is_published = Column(Boolean, nullable=False, server_default=expression.false())
    date_published = Column(TIMESTAMP, nullable=True)
    updated = Column(TIMESTAMP, nullable=False, default=datetime.now(), onupdate=datetime.now())

    def __init__(self, title, body, is_published, date_published):
        super().__init__(title, body)
        self.is_published = is_published
        self.date_published = date_published

class Page(WrittenContent):
    __tablename__ = 'pages'

    def __init__(self, title, body):
        super().__init__(title, body)

class RootFactory():
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, 'group:editors', 'edit') ]
    def __init__(self, request):
        pass
