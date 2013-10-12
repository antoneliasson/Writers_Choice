from pyramid.testing import DummyRequest
from pyramid.httpexceptions import HTTPNotFound

from writers_choice.views.view_page import view_page
from . import AbstractViewTests

class ViewPageTests(AbstractViewTests):
    def test_view_about_page(self):
        request = DummyRequest()
        request.matchdict['slug'] = 'about-us'
        response = view_page(request)
        content = response['content']
        self.assertEqual(content['title'], 'About us')
        self.assertEqual(content['body'],
                         '<p>This page contains some information about the author.</p>\n'
                         '<p>Contact: <a href="mailto:admin@example.com">Admin</a></p>')

        tab_1 = response['navigation'][0]
        self.assertEqual(tab_1['title'], 'Home')
        self.assertEqual(tab_1['url'], 'http://example.com/')
        tab_2 = response['navigation'][1]
        self.assertEqual(tab_2['title'], 'About us')
        self.assertEqual(tab_2['url'], 'http://example.com/about-us')

    def test_view_nonexistent(self):
        request = DummyRequest()
        request.matchdict['slug'] = 'nonexistent'
        response = view_page(request)
        self.assertIs(type(response), HTTPNotFound)
