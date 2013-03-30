import pyramid.testing

from ..views.view_article import view_article

from . import AbstractViewTests

class ViewArticleTests(AbstractViewTests):
    def test_view_article_1(self):
        request = pyramid.testing.DummyRequest()
        request.matchdict['id'] = 1
        info = view_article(request)
        self.assertEqual(info['title'], 'Testsida')
        self.assertEqual(info['body'],
                         '<p>Ett stycke.</p>\n<p>Ett <em>stycke</em> till.</p>')
        self.assertEqual(info['published'], '2012-01-01')
        self.assertEqual(info['edit_url'], 'http://example.com/edit/1')

    def test_view_article_2(self):
        request = pyramid.testing.DummyRequest()
        request.matchdict['id'] = 2
        info = view_article(request)
        self.assertEqual(info['title'], 'Testsida två')
        self.assertEqual(info['body'],
                         '<p>Med kod:</p>\n<pre><code>cat fil1 &gt; fil2\n'
                         '</code></pre>\n<p>och lite mer text.</p>')
        self.assertEqual(info['published'], '2012-01-03')
        self.assertEqual(info['edit_url'], 'http://example.com/edit/2')

    def test_header_levels(self):
        request = pyramid.testing.DummyRequest()
        request.matchdict['id'] = 3
        resp = view_article(request)
        self.assertEqual(resp['body'], '<p>Här finns ingenting, förutom:</p>\n<h2>Rubrik 1</h2>\n<h3>Rubrik 2</h3>')
