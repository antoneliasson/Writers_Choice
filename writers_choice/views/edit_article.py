from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from sqlalchemy.exc import DBAPIError

from ..models import (
    DBSession,
    Article,
    )

from . import slugify

@view_config(route_name='edit_article', renderer='writers_choice:templates/edit_article.pt')
def edit_article(request):
    id = request.matchdict['id']
    article = DBSession.query(Article).filter_by(id=id).one()

    if 'title' in request.params:
        title = request.params['title']
        body = request.params['body']
        article.title = title
        article.body = body
        DBSession.add(article)

        return HTTPFound(location=request.route_url('view_article_slug', id=article.id, slug=slugify(article.title)))

    submit_url = request.route_url('edit_article', id=id)
    return {'title' : article.title, 'body' : article.body, 'submit_url' : submit_url}
