from datetime import datetime, timedelta

import pyramid.testing
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from writers_choice.models import Article
from writers_choice.views.admin import edit_article

from . import AbstractViewTests

class EditArticleTests(AbstractViewTests):
    def setUp(self):
        super().setUp()
        
    def test_get(self):
        request = pyramid.testing.DummyRequest()
        request.matchdict['id'] = 2
        response = edit_article(request)

        self.assertEqual(response['title'], 'Testsida två')
        self.assertEqual(response['body'], 'Med kod:\n\n    cat fil1 > fil2\n\n'
                         'och lite mer text.')
        self.assertEqual(response['submit_url'], 'http://example.com/edit/2')
        self.assertEqual(response['message'], '')
        self.assertEqual(response['page_title'], 'Editing Testsida två — Site name')

    def test_submit_keep_published(self):
        old_id = 2
        article = self.session.query(Article).filter_by(id=old_id).one()
        old_title = article.title
        old_published = article.date_published
        new_body = 'Numera utan `kod`.'

        request = pyramid.testing.DummyRequest(
            {'title' : old_title,
             'body' : new_body,
             'save-article' : '',
             'publish' : ''}
        )
        request.matchdict['id'] = 2
        response = edit_article(request)

        article = self.session.query(Article).filter_by(id=2).one()
        self.assertEqual(article.title, old_title)
        self.assertEqual(article.body, new_body)
        self.assertTrue(article.is_published)
        self.assertEqual(article.date_published, old_published)

        self.assertIs(type(response), HTTPFound)
        self.assertEqual(response.location, 'http://example.com/edit/%d' % old_id)

    def test_submit_unpublish(self):
        old_id = 2
        article = self.session.query(Article).filter_by(id=old_id).one()
        old_title = article.title
        old_published = article.date_published
        new_body = 'Numera utan `kod`.'

        request = pyramid.testing.DummyRequest(
            {'title' : old_title,
             'body' : new_body,
             'save-article' : ''}
        )
        request.matchdict['id'] = 2
        response = edit_article(request)

        article = self.session.query(Article).filter_by(id=2).one()
        self.assertEqual(article.title, old_title)
        self.assertEqual(article.body, new_body)
        self.assertFalse(article.is_published)
        self.assertIsNone(article.date_published)

        self.assertIs(type(response), HTTPFound)
        self.assertEqual(response.location, 'http://example.com/edit/%d' % old_id)

    def test_cancel(self):
        old_id = 2
        article = self.session.query(Article).filter_by(id=old_id).one()
        old_title = article.title
        old_body = article.body
        old_published = article.date_published
        new_body = 'Numera utan `kod`.'

        request = pyramid.testing.DummyRequest(
            {'title' : old_title,
             'body' : new_body,
             'cancel-editing' : ''}
        )
        request.matchdict['id'] = 2
        response = edit_article(request)
        
        article = self.session.query(Article).filter_by(id=2).one()
        self.assertEqual(article.title, old_title)
        self.assertEqual(article.body, old_body)
        self.assertEqual(article.date_published, old_published)

        self.assertIs(type(response), HTTPFound)
        self.assertEqual(response.location,
                         'http://example.com/{}/{}/{}/testsida-tva'.format(
                             *article.date_published.timetuple()))

    def test_nonexisting(self):
        request = pyramid.testing.DummyRequest()
        request.matchdict['id'] = 9999
        response = edit_article(request)
        self.assertIs(type(response), HTTPNotFound)

    def test_strip_title_whitespace(self):
        old_id = 2
        article = self.session.query(Article).filter_by(id=old_id).one()
        old_title = article.title
        old_published = article.date_published
        old_body = article.body

        request = pyramid.testing.DummyRequest(
            {'title' : '  Rubrik\t ',
             'body' : old_body,
             'save-article' : ''}
        )
        request.matchdict['id'] = 2
        response = edit_article(request)

        article = self.session.query(Article).filter_by(id=2).one()
        self.assertEqual(article.title, 'Rubrik')

    def test_empty_title_not_acceptable(self):
        old_id = 2
        article = self.session.query(Article).filter_by(id=old_id).one()
        old_title = article.title
        old_published = article.date_published
        old_body = article.body

        request = pyramid.testing.DummyRequest(
            {'title' : '',
             'body' : 'something different\n',
             'save-article' : ''}
        )
        request.matchdict['id'] = 2
        response = edit_article(request)

        article = self.session.query(Article).filter_by(id=2).one()
        self.assertEqual(article.title, 'Testsida två')

        self.assertEqual(response['title'], old_title)
        self.assertEqual(response['body'], 'something different\n')
        self.assertFalse(response['message'] == '')

    def test_weird_newlines(self):
        old_id = 2
        article = self.session.query(Article).filter_by(id=old_id).one()
        old_title = article.title
        old_published = article.date_published
        new_body = 'Line 1\nLine 2\r\nLine 3\rLine 4\r\n\r\n'

        request = pyramid.testing.DummyRequest(
            {'title' : old_title,
             'body' : new_body,
             'save-article' : '',
             'publish' : ''}
        )
        request.matchdict['id'] = 2
        response = edit_article(request)
        
        expected = 'Line 1\nLine 2\nLine 3\nLine 4\n'
        article = self.session.query(Article).filter_by(id=2).one()
        self.assertEqual(article.title, old_title)
        self.assertEqual(article.body, expected)
        self.assertEqual(article.date_published, old_published)

    def test_publish(self):
        id = 5
        article = self.session.query(Article).filter_by(id=id).one()
        self.assertFalse(article.is_published)
        self.assertIsNone(article.date_published)
        request = pyramid.testing.DummyRequest(
            {'title' : article.title,
             'body' : article.title,
             'save-article' : '',
             'publish' : ''}
        )
        request.matchdict['id'] = id
        response = edit_article(request)

        article = self.session.query(Article).filter_by(id=id).one()
        self.assertTrue(article.is_published)
        self.assertAlmostEqual(article.date_published, datetime.now(), delta=timedelta(seconds=10))
