import pyramid.testing
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from writers_choice.views.view_article import view_article

from . import AbstractViewTests

class ViewArticleTests(AbstractViewTests):
    def test_view_article_1(self):
        request = pyramid.testing.DummyRequest()
        request.matchdict = {
            'year' : 2012,
            'month' : 1,
            'day' : 1,
            'slug' : 'testsida'
            }
        response = view_article(request)
        info = response['content']
        self.assertEqual(info['title'], 'Testsida')
        self.assertEqual(info['body'],
                         '<p>Ett stycke.</p>\n<p>Ett <em>stycke</em> till.</p>')
        self.assertEqual(info['published'], '2012-01-01')
        self.assertEqual(info['edit_url'], 'http://example.com/edit/1')

        tab_1 = response['navigation'][0]
        self.assertEqual(tab_1['title'], 'Home')
        self.assertEqual(tab_1['url'], 'http://example.com/')
        tab_2 = response['navigation'][1]
        self.assertEqual(tab_2['title'], 'About us')
        self.assertEqual(tab_2['url'], 'http://example.com/about-us')

    def test_view_article_2(self):
        request = pyramid.testing.DummyRequest()
        request.matchdict = {
            'year' : 2012,
            'month' : 1,
            'day' : 3,
            'slug' : 'testsida-tva'
            }
        response = view_article(request)
        info = response['content']
        self.assertEqual(info['title'], 'Testsida två')
        self.assertEqual(info['body'],
                         '<p>Med kod:</p>\n<pre><code>cat fil1 &gt; fil2\n'
                         '</code></pre>\n<p>och lite mer text.</p>')
        self.assertEqual(info['published'], '2012-01-03')
        self.assertEqual(info['edit_url'], 'http://example.com/edit/2')

    def test_header_levels(self):
        request = pyramid.testing.DummyRequest()
        request.matchdict = {
            'year' : 2012,
            'month' : 1,
            'day' : 2,
            'slug' : 'testsida-mittemellan'
            }
        response = view_article(request)
        info = response['content']
        self.assertEqual(info['body'], '<p>Här finns ingenting, förutom:</p>\n<h2>Rubrik 1</h2>\n<h3>Rubrik 2</h3>')

    def test_date_not_found(self):
        request = pyramid.testing.DummyRequest()
        request.matchdict = {
            'year' : 2000,
            'month' : 1,
            'day' : 1,
            'slug' : 'testsida'
            }
        response = view_article(request)
        self.assertIs(type(response), HTTPNotFound)

    def test_slug_not_found(self):
        request = pyramid.testing.DummyRequest()
        request.matchdict = {
            'year' : 2012,
            'month' : 1,
            'day' : 1,
            'slug' : 'nonexisting'
            }
        response = view_article(request)
        self.assertIs(type(response), HTTPNotFound)
