import pyramid.testing

from ..models import Article
from ..views.edit_article import edit_article

from . import AbstractViewTests

class EditArticleTests(AbstractViewTests):
    def setUp(self):
        super().setUp()
        
    def test_get(self):
        request = pyramid.testing.DummyRequest()
        request.matchdict['id'] = 2
        response = edit_article(request)

        self.assertEqual(response['title'], 'Testsida två')
        self.assertEqual(response['body'], 'Med kod:\n\n    cat fil1 > fil2\n\n'
                         'och lite mer text.')
        self.assertEqual(response['submit_url'], 'http://example.com/edit/2')

    def test_submit(self):
        old_id = 2
        article = self.session.query(Article).filter_by(id=old_id).one()
        old_title = article.title
        old_published = article.published
        new_body = 'Numera utan `kod`.'

        request = pyramid.testing.DummyRequest(
            {'title' : old_title,
             'body' : new_body}
        )
        request.matchdict['id'] = 2
        response = edit_article(request)
        

        article = self.session.query(Article).filter_by(id=2).one()
        self.assertEqual(article.title, old_title)
        self.assertEqual(article.body, new_body)
        self.assertEqual(article.published, old_published)

        from pyramid.httpexceptions import HTTPFound
        self.assertIs(type(response), HTTPFound)
        self.assertEqual(response.location, 'http://example.com/%d' % old_id)
