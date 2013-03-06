import pyramid.testing

from ..views.view_all import view_all

from . import AbstractViewTests

class ViewAllTests(AbstractViewTests):
    def test_view_all_two_articles(self):
        request = pyramid.testing.DummyRequest()
        info = view_all(request)
        self.assertEqual(len(info['articles']), 3)
        self.assertEqual(info['articles'][0]['id'], 2)
        self.assertEqual(info['articles'][0]['title'], 'Testsida två')
        self.assertEqual(info['articles'][0]['published'], '2012-01-03')

        self.assertEqual(info['articles'][1]['id'], 3)
        self.assertEqual(info['articles'][1]['title'], 'Testsida mittemellan')
        self.assertEqual(info['articles'][1]['published'], '2012-01-02')

    def test_header_levels(self):
        request = pyramid.testing.DummyRequest()
        resp = view_all(request)
        self.assertIn('<h3>Rubrik 1</h3>', resp['articles'][1]['body'])
        self.assertIn('<h4>Rubrik 2</h4>', resp['articles'][1]['body'])
