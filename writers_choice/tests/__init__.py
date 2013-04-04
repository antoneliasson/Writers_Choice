import unittest
import datetime

import pyramid.testing
import transaction
from sqlalchemy import create_engine

from ..models import (
    Base,
    Article,
    DBSession,
)

def _initTestingDB():
    engine = create_engine('sqlite://')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        article = Article(title='Testsida',
                          body='Ett stycke.\n\nEtt *stycke* till.\n',
                          published=datetime.date(2012, 1, 1))
        DBSession.add(article)
        article = Article(title='Testsida två',
                          body='Med kod:\n\n    cat fil1 > fil2\n\n'
                              'och lite mer text.',
                          published=datetime.date(2012, 1, 3))
        DBSession.add(article)
        article = Article(title='Testsida mittemellan',
                          body='Här finns ingenting, förutom:\n\nRubrik 1\n========\n\n## Rubrik 2\n',
                          published=datetime.date(2012, 1, 2))
        DBSession.add(article)
    return DBSession

class AbstractViewTests(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB()
        self.config = pyramid.testing.setUp()
        self.config.add_route('view_all', '/')
        self.config.add_route('view_article', '/{id}')
        self.config.add_route('view_article_slug', '/{id}/*slug')
        self.config.add_route('edit_article', '/edit/{id}')
        self.config.add_route('add_article', '/add')

    def tearDown(self):
        self.session.remove()
        pyramid.testing.tearDown()
