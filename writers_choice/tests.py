import unittest
import transaction

from pyramid import testing

from .models import DBSession


class TestMyView(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from .models import (
            Base,
            Article,
            )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            from datetime import date
            article = Article(title='Testsida', body='''Ett stycke.

Ett *stycke* till.''', published=date(2012, 1, 1))
            DBSession.add(article)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    # def test_it(self):
    #     from .views import my_view
    #     request = testing.DummyRequest()
    #     info = my_view(request)
    #     self.assertEqual(info['one'].name, 'one')
    #     self.assertEqual(info['project'], 'Writer\'s Choice')

    def test_article(self):
        from .models import Article
        article = DBSession.query(Article).filter(Article.id == 1).first()

        self.assertEqual(article.title, 'Testsida')
