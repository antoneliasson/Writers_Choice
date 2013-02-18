import unittest
import transaction
from datetime import date

from pyramid import testing

from sqlalchemy import create_engine

from .models import (
    Base,
    Article,
    DBSession,
)

from .models import Article

from .views.view_article import view_article
from .views.view_all import view_all
from .views.add_article import add_article
from .views.edit_article import edit_article

## Models
class ArticleTests(unittest.TestCase):
    def test_article(self):
        article = Article('Testsida',
                          body='Ett stycke.\n\nEtt *stycke* till.\n',
                          published=date(2012, 1, 1))
        self.assertEqual(article.title, 'Testsida')
        self.assertEqual(article.body, 'Ett stycke.\n\nEtt *stycke* till.\n')
        self.assertEqual(article.published, date(2012, 1, 1))

## Views
def _initTestingDB():
    engine = create_engine('sqlite://')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        article = Article(title='Testsida',
                          body='Ett stycke.\n\nEtt *stycke* till.\n',
                          published=date(2012, 1, 1))
        DBSession.add(article)
        article = Article(title='Testsida två',
                          body='Med kod:\n\n    cat fil1 > fil2\n\n'
                              'och lite mer text.',
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
        request = testing.DummyRequest()
        request.matchdict['id'] = 1
        info = view_article(request)
        self.assertEqual(info['title'], 'Testsida')
        self.assertEqual(info['body'],
                         '<p>Ett stycke.</p>\n<p>Ett <em>stycke</em> till.</p>')
        self.assertEqual(info['published'], '2012-01-01')
        self.assertEqual(info['edit_url'], 'http://example.com/edit/1')

    def test_view_article_2(self):
        request = testing.DummyRequest()
        request.matchdict['id'] = 2
        info = view_article(request)
        self.assertEqual(info['title'], 'Testsida två')
        self.assertEqual(info['body'],
                         '<p>Med kod:</p>\n<pre><code>cat fil1 &gt; fil2\n'
                         '</code></pre>\n<p>och lite mer text.</p>')
        self.assertEqual(info['published'], '2012-01-02')
        self.assertEqual(info['edit_url'], 'http://example.com/edit/2')

class ViewAllTests(AbstractViewTests):
    def test_view_all_two_articles(self):
        request = testing.DummyRequest()
        info = view_all(request)
        self.assertEqual(info['articles'][0]['title'], 'Testsida')
        self.assertEqual(info['articles'][0]['published'], '2012-01-01')
        self.assertEqual(info['articles'][1]['title'], 'Testsida två')
        self.assertEqual(info['articles'][1]['published'], '2012-01-02')

class AddArticleTests(AbstractViewTests):
    def test_not_submitted(self):
        request = testing.DummyRequest()
        info = add_article(request)
        self.assertEqual(info['submit_url'], 'http://example.com/add')

    def test_submitted(self):
        request = testing.DummyRequest(
            {'title' : 'Ny sida',
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
        request = testing.DummyRequest()
        request.matchdict['id'] = 2
        response = edit_article(request)

        self.assertEqual(response['title'], 'Testsida två')
        self.assertEqual(response['body'], 'Med kod:\n\n    cat fil1 > fil2\n\n'
                         'och lite mer text.')
        self.assertEqual(response['submit_url'], 'http://example.com/edit/2')

    def test_submit(self):
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
        res.mustcontain('<h1>Testsida</h1>', '<p>2012-01-01</p>',
                        '<p>Ett <em>stycke</em> till.</p>',
                        '<a href="http://localhost/edit/1')
    def test_visit_home(self):
        res = self.testapp.get('/', status=200)
        res.mustcontain('<h1>Testsida</h1>', '<h1>Testsida två</h1>',
                        '<a href="http://localhost/add')
    def test_add_article(self):
        res = self.testapp.get('/add', status=200)
        res.mustcontain('<h1 class="title">'
                            '<input type="text" name="title" value="" /></h1>',
                        '<form action="http://localhost/add" method="post"',
                        '<input type="text" name="title"', '<textarea name="body"',
                        '<input type="submit"')
        res = self.testapp.post('/add', {'title' : 'Ny sida', 'body' : 'Brödtext.'},
                                status=302)
        res = res.follow()
        res.mustcontain('<h1>Ny sida</h1>')

    def test_edit_article(self):
        res = self.testapp.get('/edit/1', status=200)
        res.mustcontain('<form action="http://localhost/edit/1" method="post"',
                        '<h1 class="title">',
                        '<input type="text" name="title" value="Testsida"',
                        '<textarea name="body">Ett stycke.\n\n'
                            'Ett *stycke* till.\n</textarea>',
                        '<input type="submit"')

        res = self.testapp.post('/edit/1',
                                {'title' : 'Testande sida', 'body' : 'text.\n'},
                                status=302)
        res = res.follow()
        res.mustcontain('<h1>Testande sida</h1>')
