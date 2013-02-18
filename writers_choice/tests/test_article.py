import unittest
import datetime

from ..models import Article

class ArticleTests(unittest.TestCase):
    def test_article(self):
        article = Article('Testsida',
                          body='Ett stycke.\n\nEtt *stycke* till.\n',
                          published=datetime.date(2012, 1, 1))
        self.assertEqual(article.title, 'Testsida')
        self.assertEqual(article.body, 'Ett stycke.\n\nEtt *stycke* till.\n')
        self.assertEqual(article.published, datetime.date(2012, 1, 1))

