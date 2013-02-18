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
        self.assertEqual(info['published'], '2012-01-02')
        self.assertEqual(info['edit_url'], 'http://example.com/edit/2')
