import unittest
import datetime

from ..models import Article#, Editor

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

# class EditorTests(unittest.TestCase):
#     def test_editor(self):
#         editor = Editor(email='editor@example.com',
#                         joined=datetime.date(2013, 1, 1))
#         self.assertEqual(editor.email, 'editor@example.com')
#         self.assertEqual(editor.joined, datetime.date(2013, 1, 1))
