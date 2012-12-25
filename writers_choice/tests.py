import unittest
import transaction
from datetime import date

from pyramid import testing

def _initTestingDB():
    from sqlalchemy import create_engine
    engine = create_engine('sqlite://')
    from .models import (
        Base,
        Article,
        DBSession,
    )
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        article = Article(title='Testsida',
                          body='Ett stycke.\n\nEtt *stycke* till.\n',
                          published=date(2012, 1, 1))
        DBSession.add(article)
        article = Article(title='Testsida två',
                          body='Med kod:\n\n    cat fil1 > fil2\n\noch lite mer text.',
                          published=date(2012, 1, 2))
        DBSession.add(article)
    return DBSession

class ArticleTests(unittest.TestCase):
    def test_article(self):
        from .models import Article
        article = Article('Testsida',
                          body='Ett stycke.\n\nEtt *stycke* till.\n',
                          published=date(2012, 1, 1))
        self.assertEqual(article.title, 'Testsida')
        self.assertEqual(article.body, 'Ett stycke.\n\nEtt *stycke* till.\n')
        self.assertEqual(article.published, date(2012, 1, 1))

class ViewArticleTests(unittest.TestCase):
    def setUp(self):
#        self.config = testing.setUp()
        self.session = _initTestingDB()

    def tearDown(self):
        self.session.remove()
#        testing.tearDown()

    def test_view_article1(self):
        from .views import view_article
        request = testing.DummyRequest()
        request.matchdict['id'] = 1
        info = view_article(request)
        self.assertEqual(info['title'], 'Testsida')
        self.assertEqual(info['body'],
                         '<p>Ett stycke.</p>\n<p>Ett <em>stycke</em> till.</p>')
        self.assertEqual(info['published'], '2012-01-01')

    def test_view_article2(self):
        from .views import view_article
        request = testing.DummyRequest()
        request.matchdict['id'] = 2
        info = view_article(request)
        self.assertEqual(info['title'], 'Testsida två')
        self.assertEqual(info['body'],
                         '<p>Med kod:</p>\n<pre><code>cat fil1 &gt; fil2\n</code></pre>\n<p>och lite mer text.</p>')
        self.assertEqual(info['published'], '2012-01-02')

class ViewAllTests(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB()

    def tearDown(self):
        self.session.remove()

    def test_view_all(self):
        from .views import view_all
        request = testing.DummyRequest()
        info = view_all(request)
        self.assertEqual(info['articles'][0]['title'], 'Testsida')
        self.assertEqual(info['articles'][0]['published'], '2012-01-01')
        self.assertEqual(info['articles'][1]['title'], 'Testsida två')
        self.assertEqual(info['articles'][1]['published'], '2012-01-02')

class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from writers_choice import main
        settings = { 'sqlalchemy.url': 'sqlite://'}
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)
        self.session = _initTestingDB()

    def tearDown(self):
        self.session.remove()

    def test_visit_article1(self):
        res = self.testapp.get('/1', status=200)
        self.assertIn(b'<h1>Testsida</h1>', res.body)
        self.assertIn(b'<p>2012-01-01</p>', res.body)
        self.assertIn(b'<p>Ett <em>stycke</em> till.</p>', res.body)

    def test_visit_home(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'<h1>Testsida</h1>', res.body)
        self.assertIn('<h1>Testsida två</h1>', res.body.decode('utf-8'))
