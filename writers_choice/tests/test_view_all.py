import pyramid.testing

from ..views.view_all import view_all

from . import AbstractViewTests

class ViewAllTests(AbstractViewTests):
    def test_view_all_two_articles(self):
        request = pyramid.testing.DummyRequest()
        info = view_all(request)
        self.assertEqual(len(info['articles']), 3)
        self.assertEqual(info['articles'][0]['title'], 'Testsida')
        self.assertEqual(info['articles'][0]['published'], '2012-01-01')
        self.assertEqual(info['articles'][1]['title'], 'Testsida två')
        self.assertEqual(info['articles'][1]['published'], '2012-01-03')
