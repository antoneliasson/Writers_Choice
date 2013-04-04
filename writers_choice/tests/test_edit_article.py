import pyramid.testing
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from ..models import Article
from ..views.edit_article import edit_article

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

    def test_submit(self):
        old_id = 2
        article = self.session.query(Article).filter_by(id=old_id).one()
        old_title = article.title
        old_published = article.published
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
        self.assertEqual(article.published, old_published)

        self.assertIs(type(response), HTTPFound)
        self.assertEqual(response.location, 'http://example.com/%d/testsida-tva' % old_id)

    def test_cancel(self):
        old_id = 2
        article = self.session.query(Article).filter_by(id=old_id).one()
        old_title = article.title
        old_body = article.body
        old_published = article.published
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
        self.assertEqual(article.published, old_published)

        self.assertIs(type(response), HTTPFound)
        self.assertEqual(response.location, 'http://example.com/%d/testsida-tva' % old_id)

    def test_nonexisting(self):
        request = pyramid.testing.DummyRequest()
        request.matchdict['id'] = 9999
        response = edit_article(request)
        self.assertIs(type(response), HTTPNotFound)

    def test_strip_title_whitespace(self):
        old_id = 2
        article = self.session.query(Article).filter_by(id=old_id).one()
        old_title = article.title
        old_published = article.published
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

        self.assertIs(type(response), HTTPFound)
        self.assertEqual(response.location, 'http://example.com/%d/rubrik' % old_id)

    def test_empty_title_not_acceptable(self):
        old_id = 2
        article = self.session.query(Article).filter_by(id=old_id).one()
        old_title = article.title
        old_published = article.published
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
