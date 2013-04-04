from datetime import datetime

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from ..models import (
    DBSession,
    Article,
    )

from . import slugify

@view_config(route_name='add_article', renderer='writers_choice:templates/edit_article.pt')
def add_article(request):
    if 'save-article' in request.params:
        title = request.params['title']
        body = request.params['body']
        published = datetime.now()
        article = Article(title, body, published)
        DBSession.add(article)
        # let the DB fill in the id
        DBSession.flush()

        return HTTPFound(location=request.route_url('view_article_slug', id=article.id, slug=slugify(article.title)))
    elif 'cancel-editing' in request.params:
        return HTTPFound(location=request.route_url('view_all'))

    submit_url = request.route_url('add_article')
    return {'title' : '', 'body' : '', 'submit_url' : submit_url}
