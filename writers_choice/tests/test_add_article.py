import pyramid.testing
from pyramid.httpexceptions import HTTPFound

from ..models import Article
from ..views.add_article import add_article

from . import AbstractViewTests

class AddArticleTests(AbstractViewTests):
    def test_not_submitted(self):
        request = pyramid.testing.DummyRequest()
        resp = add_article(request)
        self.assertEqual(resp['submit_url'], 'http://example.com/add')

    def test_submitted(self):
        request = pyramid.testing.DummyRequest(
            {'title' : 'Ny sida',
             'body' : 'Brödtext.',
             'save-article' : ''}
        )
        resp = add_article(request)

        article = self.session.query(Article).filter_by(title='Ny sida').first()
        self.assertEqual(article.title, 'Ny sida')
        self.assertEqual(article.body, 'Brödtext.')

        self.assertIs(type(resp), HTTPFound)
        self.assertEqual(resp.location, 'http://example.com/%d/ny-sida' % article.id)

    def test_cancel(self):
        request = pyramid.testing.DummyRequest(
            {'title' : 'Ny sida',
             'body' : 'Brödtext.',
             'cancel-editing' : ''}
        )
        resp = add_article(request)

        article_count = self.session.query(Article).filter_by(title='Ny sida').count()
        self.assertEqual(article_count, 0)

        self.assertIs(type(resp), HTTPFound)
        self.assertEqual(resp.location, 'http://example.com/')
