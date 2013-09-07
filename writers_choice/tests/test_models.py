import unittest
import datetime

from writers_choice.models import Article, Page#, Editor

class ArticleTests(unittest.TestCase):
    def test_article(self):
        article = Article('Testsida',
                          body='Ett stycke.\n\nEtt *stycke* till.\n',
                          is_published=True,
                          date_published=datetime.date(2012, 1, 1))
        self.assertEqual(article.title, 'Testsida')
        self.assertEqual(article.body, 'Ett stycke.\n\nEtt *stycke* till.')
        self.assertEqual(article.is_published, True)
        self.assertEqual(article.date_published, datetime.date(2012, 1, 1))

class PageTests(unittest.TestCase):
    def test_page(self):
        body = 'This page contains som information about the author.\n\n'\
        'Contact: [Admin](mailto:admin@example.com)'

        page = Page(title='About', body=body)
        self.assertEqual(page.title, 'About')
        self.assertEqual(page.body, body)
        self.assertEqual(page.slug, 'about')

    def test_change_title(self):
        page = Page(title='About', body='body text')
        self.assertEqual(page.title, 'About')
        self.assertEqual(page.slug, 'about')
        page.title = 'About Me'
        self.assertEqual(page.title, 'About Me')
        self.assertEqual(page.slug, 'about')

# class EditorTests(unittest.TestCase):
#     def test_editor(self):
#         editor = Editor(email='editor@example.com',
#                         joined=datetime.date(2013, 1, 1))
#         self.assertEqual(editor.email, 'editor@example.com')
#         self.assertEqual(editor.joined, datetime.date(2013, 1, 1))
