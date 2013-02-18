import pyramid.testing

from ..models import Article
from ..views.add_article import add_article

from . import AbstractViewTests

class AddArticleTests(AbstractViewTests):
    def test_not_submitted(self):
        request = pyramid.testing.DummyRequest()
        info = add_article(request)
        self.assertEqual(info['submit_url'], 'http://example.com/add')

    def test_submitted(self):
        request = pyramid.testing.DummyRequest(
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
