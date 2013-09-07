import unittest
import datetime

import pyramid.testing
import transaction
from sqlalchemy import create_engine

from ..models import (
    Base,
    Article,
    Page,
    DBSession,
)

def _initTestingDB():
    engine = create_engine('sqlite://')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        article = Article(title='Testsida',
                          body='Ett stycke.\n\nEtt *stycke* till.\n',
                          is_published=True,
                          date_published=datetime.date(2012, 1, 1))
        DBSession.add(article)
        article = Article(title='Testsida två',
                          body='Med kod:\n\n    cat fil1 > fil2\n\n'
                              'och lite mer text.',
                          is_published=True,
                          date_published=datetime.date(2012, 1, 3))
        DBSession.add(article)
        article = Article(title='Testsida mittemellan',
                          body='Här finns ingenting, förutom:\n\nRubrik 1\n========\n\n## Rubrik 2\n',
                          is_published=True,
                          date_published=datetime.date(2012, 1, 2))
        DBSession.add(article)
        article = Article(title='<i>HTML-title</i>',
                          body='<strong>Nice HTML</strong> and\n\n<script>document.write("<p>Evil HTML</p>");</script>',
                          is_published=True,
                          date_published=datetime.date(2011, 1, 2))
        DBSession.add(article)
        article = Article(title='Unpublished article',
                          body='This is an article that has not yet been published.',
                          is_published=False,
                          date_published=None)
        DBSession.add(article)

        page = Page(title='About us',
                    body='This page contains som information about the author.\n\n'\
                    'Contact: [Admin](mailto:admin@example.com)')
        DBSession.add(page)

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
        self.config.add_route('view_page', '/{slug}')
        self.config.add_settings(site_name='Site name')

    def tearDown(self):
        self.session.remove()
        pyramid.testing.tearDown()
