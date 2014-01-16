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
        self.body = body
        self.slug = make_slug(self.title)

    @property
    def body(self): return self._body
    @body.setter
    def body(self, value): self._body = '\n'.join(value.splitlines())

class Article(WrittenContent):
    __tablename__ = 'articles'

    is_published = Column(Boolean, nullable=False, server_default=expression.false())
    date_published = Column(TIMESTAMP, nullable=True)
    updated = Column(TIMESTAMP, nullable=False, default=datetime.now(), onupdate=datetime.now())

    def __init__(self, title, body, is_published, date_published):
        super().__init__(title, body)
        self.is_published = is_published
        self.date_published = date_published

    def get_url(self, request):
        year, month, day = self.date_published.timetuple()[:3]
        return request.route_url('view_article',
                                 year=year,
                                 month=month,
                                 day=day,
                                 slug=self.slug)

    def get_edit_url(self, request):
        return request.route_url('edit_article', id=self.id)

class Page(WrittenContent):
    __tablename__ = 'pages'

    def __init__(self, title, body):
        super().__init__(title, body)

class RootFactory():
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, 'group:editors', 'edit') ]
    def __init__(self, request):
        pass
