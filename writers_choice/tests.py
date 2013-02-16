import unittest
import transaction
from datetime import date

from pyramid import testing

## Models
class ArticleTests(unittest.TestCase):
    def test_article(self):
        from .models import Article
        article = Article('Testsida',
                          body='Ett stycke.\n\nEtt *stycke* till.\n',
                          published=date(2012, 1, 1))
        self.assertEqual(article.title, 'Testsida')
        self.assertEqual(article.body, 'Ett stycke.\n\nEtt *stycke* till.\n')
        self.assertEqual(article.published, date(2012, 1, 1))

## Views
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

class AbstractViewTests(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()
        self.config.add_route('view_article', '/{id}')
        self.config.add_route('edit_article', '/edit/{id}')
        self.config.add_route('add_article', '/add')

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

class ViewArticleTests(AbstractViewTests):
    def test_view_article_1(self):
        from .views import view_article
        request = testing.DummyRequest()
        request.matchdict['id'] = 1
        info = view_article(request)
        self.assertEqual(info['title'], 'Testsida')
        self.assertEqual(info['body'],
                         '<p>Ett stycke.</p>\n<p>Ett <em>stycke</em> till.</p>')
        self.assertEqual(info['published'], '2012-01-01')
        self.assertEqual(info['edit_url'], 'http://example.com/edit/1')

    def test_view_article_2(self):
        from .views import view_article
        request = testing.DummyRequest()
        request.matchdict['id'] = 2
        info = view_article(request)
        self.assertEqual(info['title'], 'Testsida två')
        self.assertEqual(info['body'],
                         '<p>Med kod:</p>\n<pre><code>cat fil1 &gt; fil2\n</code></pre>\n<p>och lite mer text.</p>')
        self.assertEqual(info['published'], '2012-01-02')
        self.assertEqual(info['edit_url'], 'http://example.com/edit/2')

class ViewAllTests(AbstractViewTests):
    def test_view_all_two_articles(self):
        from .views import view_all
        request = testing.DummyRequest()
        info = view_all(request)
        self.assertEqual(info['articles'][0]['title'], 'Testsida')
        self.assertEqual(info['articles'][0]['published'], '2012-01-01')
        self.assertEqual(info['articles'][1]['title'], 'Testsida två')
        self.assertEqual(info['articles'][1]['published'], '2012-01-02')

class AddArticleTests(AbstractViewTests):
    def test_not_submitted(self):
        from .views import add_article
        request = testing.DummyRequest()
        info = add_article(request)
        self.assertEqual(info['submit_url'], 'http://example.com/add')

    def test_submitted(self):
        from .views import add_article
        from .models import Article

        request = testing.DummyRequest(
            {'form.submitted' : True,
             'title' : 'Ny sida',
             'body' : 'Brödtext.'}
        )
        info = add_article(request)

        article = self.session.query(Article).filter_by(title='Ny sida').first()
        self.assertEqual(article.title, 'Ny sida')
        self.assertEqual(article.body, 'Brödtext.')

        from pyramid.httpexceptions import HTTPFound
        self.assertIs(type(info), HTTPFound)
        self.assertEqual(info.location, 'http://example.com/%d' % article.id)

class EditArticleTests(AbstractViewTests):
    def setUp(self):
        super().setUp()
        
    def test_get(self):
        from .views import edit_article

        request = testing.DummyRequest()
        request.matchdict['id'] = 2
        response = edit_article(request)

        self.assertEqual(response['title'], 'Testsida två')
        self.assertEqual(response['body'], 'Med kod:\n\n    cat fil1 > fil2\n\noch lite mer text.')
        self.assertEqual(response['submit_url'], 'http://example.com/edit/2')

    def test_submit(self):
        from .views import edit_article
        from .models import Article

        old_id = 2
        article = self.session.query(Article).filter_by(id=old_id).one()
        old_title = article.title
        old_published = article.published
        new_body = 'Numera utan `kod`.'

        request = testing.DummyRequest(
            {'title' : old_title,
             'body' : new_body}
        )
        request.matchdict['id'] = 2
        response = edit_article(request)
        

        article = self.session.query(Article).filter_by(id=2).one()
        self.assertEqual(article.title, old_title)
        self.assertEqual(article.body, new_body)
        self.assertEqual(article.published, old_published)

        from pyramid.httpexceptions import HTTPFound
        self.assertIs(type(response), HTTPFound)
        self.assertEqual(response.location, 'http://example.com/%d' % old_id)

## Functional tests
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

    def test_visit_article_1(self):
        res = self.testapp.get('/1', status=200)
        self.assertIn(b'<h1>Testsida</h1>', res.body)
        self.assertIn(b'<p>2012-01-01</p>', res.body)
        self.assertIn(b'<p>Ett <em>stycke</em> till.</p>', res.body)
        self.assertIn(b'<a href="http://localhost/edit/1', res.body)

    def test_visit_home(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'<h1>Testsida</h1>', res.body)
        self.assertIn('<h1>Testsida två</h1>', res.body.decode('utf-8'))
        self.assertIn(b'<a href="http://localhost/add', res.body)

    def test_add_article(self):
        res = self.testapp.get('/add', status=200)
        self.assertIn(b'<h1>Add article</h1>', res.body)
        self.assertIn(b'<form action="http://localhost/add" method="post"', res.body)
        self.assertIn(b'<input type="text" name="title"', res.body)
        self.assertIn(b'<textarea name="body"', res.body)
        self.assertIn(b'<input type="submit"', res.body)

        res = self.testapp.post('/add', {'title' : 'Ny sida', 'body' : 'Brödtext.'}, status=302)
        res = res.follow()
        self.assertIn(b'<h1>Ny sida</h1>', res.body)

    def test_edit_article(self):
        res = self.testapp.get('/edit/1', status=200)
        self.assertIn(b'<form action="http://localhost/edit/1" method="post"', res.body)
        self.assertIn(b'<h1 class="title">'
                      b'<input type="text" name="title" value="Testsida"', res.body)
        self.assertIn(b'<textarea name="body">Ett stycke.\n\nEtt *stycke* till.\n'
                      b'</textarea>', res.body)
        self.assertIn(b'<input type="submit"', res.body)

        res = self.testapp.post('/edit/1', {'title' : 'Testande sida', 'body' : 'text.\n'},
                                status=302)
        res = res.follow()
        self.assertIn(b'<h1>Testande sida</h1>', res.body)
