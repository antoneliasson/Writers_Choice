from pyramid.testing import DummyRequest
from pyramid.httpexceptions import HTTPNotFound

from writers_choice.views.view_page import view_page
from . import AbstractViewTests

class ViewPageTests(AbstractViewTests):
    def test_view_about_page(self):
        request = DummyRequest()
        request.matchdict['slug'] = 'about'
        response = view_page(request)
        content = response['content']
        self.assertEqual(content['title'], 'About')
        self.assertEqual(content['body'],
                         '<p>This page contains som information about the author.</p>\n'
                         '<p>Contact: <a href="mailto:admin@example.com">Admin</a></p>')

    def test_view_nonexistent(self):
        request = DummyRequest()
        request.matchdict['slug'] = 'nonexistent'
        response = view_page(request)
        self.assertIs(type(response), HTTPNotFound)
