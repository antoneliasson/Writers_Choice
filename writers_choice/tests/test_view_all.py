import pyramid.testing

from ..views.view_all import view_all

from . import AbstractViewTests

class ViewAllTests(AbstractViewTests):
    def test_view_all_two_articles(self):
        request = pyramid.testing.DummyRequest()
        resp = view_all(request)
        self.assertEqual(len(resp['articles']), 4)

        article_2 = resp['articles'][0]
        self.assertEqual(article_2['id'], 2)
        self.assertEqual(article_2['title'], 'Testsida två')
        self.assertEqual(article_2['published'], '2012-01-03')
        self.assertEqual(article_2['url'], 'http://example.com/2/testsida-tva')

        article_3 = resp['articles'][1]
        self.assertEqual(article_3['id'], 3)
        self.assertEqual(article_3['title'], 'Testsida mittemellan')
        self.assertEqual(article_3['published'], '2012-01-02')
        self.assertEqual(article_3['url'], 'http://example.com/3/testsida-mittemellan')

    def test_header_levels(self):
        request = pyramid.testing.DummyRequest()
        resp = view_all(request)
        self.assertIn('<h3>Rubrik 1</h3>', resp['articles'][1]['body'])
        self.assertIn('<h4>Rubrik 2</h4>', resp['articles'][1]['body'])
