import unittest
import transaction
from pyramid import testing


from . import _initTestingDB

class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from writers_choice import main
        settings = { 'sqlalchemy.url': 'sqlite://'}
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)
        self.session = _initTestingDB()

    def tearDown(self):
        self.session.remove()

    def test_visit_article_1(self):
        res = self.testapp.get('/1/testsida', status=200)
        res.mustcontain('<h1>Testsida</h1>', '<p>2012-01-01</p>',
                        '<p>Ett <em>stycke</em> till.</p>',
                        '<a href="http://localhost/edit/1')
    def test_visit_home(self):
        res = self.testapp.get('/', status=200)
        res.mustcontain('<h1><a href="http://localhost/">Writer&apos;s Choice</a></h1>',
                        '<h2><a href="http://localhost/1/testsida">Testsida</a></h2>',
                        '<h2><a href="http://localhost/2/testsida-tva">Testsida två</a></h2>',
                        '<h3>Rubrik 1</h3>',
                        '<a href="http://localhost/add')
    def test_add_article(self):
        res = self.testapp.get('/add', status=200)
        res.mustcontain('<h1 class="title">'
                            '<input type="text" name="title" value="" /></h1>',
                        '<form action="http://localhost/add" method="post"',
                        '<input type="text" name="title"', '<textarea name="body"',
                        '<input type="submit"')
        res = self.testapp.post('/add', {'title' : 'Ny sida', 'body' : 'Brödtext.'},
                                status=302)
        res = res.follow()
        res.mustcontain('<h1>Ny sida</h1>')

    def test_edit_article(self):
        res = self.testapp.get('/edit/1', status=200)
        res.mustcontain('<form action="http://localhost/edit/1" method="post"',
                        '<h1 class="title">',
                        '<input type="text" name="title" value="Testsida"',
                        '<textarea name="body">Ett stycke.\n\n'
                            'Ett *stycke* till.\n</textarea>',
                        '<input type="submit"')

        res = self.testapp.post('/edit/1',
                                {'title' : 'Testande sida', 'body' : 'text.\n'},
                                status=302)
        res = res.follow()
        res.mustcontain('<h1>Testande sida</h1>')
