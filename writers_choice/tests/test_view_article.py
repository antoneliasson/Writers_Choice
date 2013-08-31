import pyramid.testing
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from ..views.view_article import view_article

from . import AbstractViewTests

class ViewArticleTests(AbstractViewTests):
    def test_view_article_1(self):
        request = pyramid.testing.DummyRequest()
        request.matchdict['id'] = 1
        request.matchdict['slug'] = 'testsida'
        response = view_article(request)
        info = response['article']
        self.assertEqual(info['title'], 'Testsida')
        self.assertEqual(info['body'],
                         '<p>Ett stycke.</p>\n<p>Ett <em>stycke</em> till.</p>')
        self.assertEqual(info['published'], '2012-01-01')
        self.assertEqual(info['edit_url'], 'http://example.com/edit/1')

    def test_view_article_2(self):
        request = pyramid.testing.DummyRequest()
        request.matchdict['id'] = 2
        request.matchdict['slug'] = 'testsida-tva'
        response = view_article(request)
        info = response['article']
        self.assertEqual(info['title'], 'Testsida två')
        self.assertEqual(info['body'],
                         '<p>Med kod:</p>\n<pre><code>cat fil1 &gt; fil2\n'
                         '</code></pre>\n<p>och lite mer text.</p>')
        self.assertEqual(info['published'], '2012-01-03')
        self.assertEqual(info['edit_url'], 'http://example.com/edit/2')

    def test_header_levels(self):
        request = pyramid.testing.DummyRequest()
        request.matchdict['id'] = 3
        request.matchdict['slug'] = 'testsida-mittemellan'
        response = view_article(request)
        info = response['article']
        self.assertEqual(info['body'], '<p>Här finns ingenting, förutom:</p>\n<h2>Rubrik 1</h2>\n<h3>Rubrik 2</h3>')

    def test_no_slug(self):
        request = pyramid.testing.DummyRequest()
        request.matchdict['id'] = 2
        response = view_article(request)
        self.assertIs(type(response), HTTPFound)
        self.assertEqual(response.location, 'http://example.com/2/testsida-tva')

    def test_empty_slug(self):
        request = pyramid.testing.DummyRequest()
        request.matchdict['id'] = 2
        request.matchdict['slug'] = ()
        response = view_article(request)
        self.assertIs(type(response), HTTPFound)
        self.assertEqual(response.location, 'http://example.com/2/testsida-tva')

    def test_wrong_slug(self):
        request = pyramid.testing.DummyRequest()
        request.matchdict['id'] = 2
        request.matchdict['slug'] = ('fel-sida',)
        response = view_article(request)
        self.assertIs(type(response), HTTPFound)
        self.assertEqual(response.location, 'http://example.com/2/testsida-tva')

    def test_not_found(self):
        request = pyramid.testing.DummyRequest()
        request.matchdict['id'] = 9999
        response = view_article(request)
        self.assertIs(type(response), HTTPNotFound)

    def test_unpublished(self):
        request = pyramid.testing.DummyRequest()
        request.matchdict['id'] = 5
        response = view_article(request)
        self.assertIs(type(response), HTTPNotFound)
