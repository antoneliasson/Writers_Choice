import unittest
import transaction
from pyramid import testing

import re
import urllib.parse
import requests

from . import _initTestingDB

AUDIENCE = 'http://example.com'

class FunctionalTests(unittest.TestCase):
    def getAssertion():
        ''' Grabs a valid identity assertion from personatestuser.org for testing '''
        url = 'http://personatestuser.org/email_with_assertion/{}'.format(
            urllib.parse.quote(AUDIENCE, safe=''))
        response = requests.get(url)
        persona = response.json()

        return (persona['email'], persona['pass'], persona['assertion'])

    def authenticate():
        ''' Authenticates using Persona. Not used currently. '''
        res = self.testapp.get('/add', status=403)
        # this plucks the csrf token from the Javascript form in the 403 response body
        match = re.search('<input type=\'hidden\'[\s"\+]+name=\'csrf_token\'[\s"\+]+value=\'(?P<csrf>[a-z0-9]+)\'\s+/>', res.text)
        csrf_token = match.group('csrf')
        res = self.testapp.post('/login', {'assertion' : FunctionalTests.assertion, 'came_from' : 'http://localhost:6543/add', 'csrf_token' : csrf_token}, status=302)
        print(self.testapp.cookies)
        self.assertEqual(res.headers['Location'], 'http://localhost:6543/add')
        self.fail()

    def setUp(self):
        settings = {'sqlalchemy.url': 'sqlite://',
                    'site_name' : 'Site name',
                    'admin_email' : 'admin@example.com',
                    'RemoteUserAuthenticationPolicy' : ''}
        from writers_choice import main
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app, extra_environ={'REMOTE_USER' : settings['admin_email']})
        self.session = _initTestingDB()

    def tearDown(self):
        self.session.remove()

    def test_visit_article_1(self):
        res = self.testapp.get('/1/testsida', status=200)
        res.mustcontain('<title>Testsida — Site name</title>',
                        '<a href="http://localhost/" id="banner">Site name</a>',
                        '<h1>Testsida</h1>', '<p>2012-01-01</p>',
                        '<p>Ett <em>stycke</em> till.</p>',
                        '<a href="http://localhost/edit/1')

    def test_visit_evil_article(self):
        res = self.testapp.get('/4/ihtml-titlei', status=200)
        res.mustcontain('>&lt;i&gt;HTML-title&lt;/i&gt;</h1>')

    def test_visit_nonexisting_article(self):
        resp = self.testapp.get('/9999', status=404)
        resp.mustcontain('No such article.')

    def test_visit_home(self):
        res = self.testapp.get('/', status=200)
        res.mustcontain('<title>Site name</title>',
                        '<a href="http://localhost/" id="banner">Site name</a>',
                        '<h1>Blog</h1>',
                        '<h2><a href="http://localhost/1/testsida">Testsida</a></h2>',
                        '<h2><a href="http://localhost/2/testsida-tva">Testsida två</a></h2>',
                        '<h3>Rubrik 1</h3>',
                        '<a href="http://localhost/add',
                        '>&lt;i&gt;HTML-title&lt;/i&gt;</a></h2>')

    def test_visit_home_unauthorized(self):
        res = self.testapp.get('/', status=200, extra_environ={'REMOTE_USER' : 'nobody@example.com'})
        self.assertNotIn('<a href="http://localhost/add', res)

    def test_visit_article_1_unauthorized(self):
        res = self.testapp.get('/1/testsida', status=200, extra_environ={'REMOTE_USER' : 'nobody@example.com'})
        self.assertNotIn('<a href="http://localhost/edit/1', res)

    def test_add_article(self):
        res = self.testapp.get('/add', status=200)
        res.mustcontain('<title>New article — Site name</title>',
                        '<a href="http://localhost/" id="banner">Site name</a>',
                        '<h1 class="title"><input type="text" name="title" value=""',
                        '<form action="http://localhost/add" method="post"',
                        '<textarea name="body"',
                        '<input type="submit"')
        res = self.testapp.post('/add', {'title' : 'Ny sida', 'body' : 'Brödtext.',
                                         'save-article' : ''},
                                status=302)
        res = res.follow()
        res.mustcontain('<h1>Ny sida</h1>')

    def test_edit_article(self):
        res = self.testapp.get('/edit/1', status=200)
        res.mustcontain('<title>Editing Testsida — Site name</title>',
                        '<a href="http://localhost/" id="banner">Site name</a>',
                        '<form action="http://localhost/edit/1" method="post"',
                        '<h1 class="title">',
                        '<input type="text" name="title" value="Testsida"',
                        '>Ett stycke.\n\n'
                            'Ett *stycke* till.</textarea>',
                        '<input type="submit"')

        res = self.testapp.post('/edit/1',
                                {'title' : 'Testande sida',
                                 'body' : 'text.\n',
                                 'save-article' : ''},
                                status=302)
        res = res.follow()
        res.mustcontain('<h1>Testande sida</h1>')

    def test_add_article_empty_title(self):
        res = self.testapp.post('/add', {'title' : '',
                                         'body' : 'Brödtext.',
                                         'save-article' : ''},
                                status=200)
        res.mustcontain('>Brödtext.</textarea>',
                        '<p class="message">')

    def test_edit_article_empty_title(self):
        res = self.testapp.post('/edit/1',
                                {'title' : '',
                                 'body' : 'text.\n',
                                 'save-article' : ''},
                                status=200)
        res.mustcontain('>text.\n</textarea>',
                        '<p class="message">')
