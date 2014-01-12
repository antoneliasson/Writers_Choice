from datetime import datetime, timedelta

import pyramid.testing
from pyramid.httpexceptions import HTTPFound

from writers_choice.models import Article
from writers_choice.views.admin import add_article

from . import AbstractViewTests

class AddArticleTests(AbstractViewTests):
    def test_not_submitted(self):
        request = pyramid.testing.DummyRequest()
        resp = add_article(request)
        self.assertEqual(resp['title'], '')
        self.assertEqual(resp['body'], '')
        self.assertEqual(resp['submit_url'], 'http://example.com/add')
        self.assertEqual(resp['message'], '')
        self.assertEqual(resp['page_title'], 'New article — Site name')

    def test_submitted_not_published(self):
        request = pyramid.testing.DummyRequest(
            {'title' : 'Ny sida',
             'body' : 'Brödtext.',
             'save-article' : ''}
        )
        resp = add_article(request)

        article = self.session.query(Article).filter_by(title='Ny sida').one()
        self.assertEqual(article.title, 'Ny sida')
        self.assertEqual(article.body, 'Brödtext.')
        self.assertFalse(article.is_published)
        self.assertIsNone(article.date_published)

        self.assertIs(type(resp), HTTPFound)
        self.assertEqual(resp.location, 'http://example.com/edit/{}'.format(article.id))

    def test_submitted_published(self):
        request = pyramid.testing.DummyRequest(
            {'title' : 'Ny sida',
             'body' : 'Brödtext.',
             'publish' : '',
             'save-article' : ''}
        )
        resp = add_article(request)

        article = self.session.query(Article).filter_by(title='Ny sida').one()
        self.assertEqual(article.title, 'Ny sida')
        self.assertEqual(article.body, 'Brödtext.')
        self.assertTrue(article.is_published)
        self.assertAlmostEqual(article.date_published,
                               datetime.now(),
                               delta=timedelta(seconds=10))

        self.assertIs(type(resp), HTTPFound)
        self.assertEqual(resp.location, 'http://example.com/edit/{}'.format(article.id))

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

    def test_strip_title_whitespace(self):
        request = pyramid.testing.DummyRequest(
            {'title' : '  Rubrik\t ',
             'body' : 'Brödtext.',
             'save-article' : ''}
        )
        resp = add_article(request)

        article_count = self.session.query(Article).filter_by(title='Rubrik').count()
        self.assertEqual(article_count, 1)

    def test_empty_title_not_acceptable(self):
        request = pyramid.testing.DummyRequest(
            {'title' : '',
             'body' : 'Brödtext.',
             'save-article' : None}
        )
        resp = add_article(request)

        article_count = self.session.query(Article).filter_by(title='').count()
        self.assertEqual(article_count, 0)

        self.assertEqual(resp['title'], '')
        self.assertEqual(resp['body'], 'Brödtext.')
        self.assertFalse(resp['message'] == '')

    def test_newline_normalization(self):
        request = pyramid.testing.DummyRequest(
            {'title' : 'Article with weird newline chars',
             'body' : 'Line 1\nLine 2\r\nLine 3\rLine 4\r\n\r\n',
             'save-article' : None}
        )
        resp = add_article(request)

        expected = 'Line 1\nLine 2\nLine 3\nLine 4\n'
        article = self.session.query(Article).filter_by(
            title='Article with weird newline chars').one()
        self.assertEqual(article.body, expected)
