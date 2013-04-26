from markdown import markdown

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from sqlalchemy.exc import DBAPIError

from ..models import (
    DBSession,
    Article,
    )

from . import format_article_metadata, slugify

@view_config(route_name='view_article_noslug', renderer='writers_choice:templates/view_article.pt', permission='view')
@view_config(route_name='view_article_slug', renderer='writers_choice:templates/view_article.pt', permission='view')
def view_article(request):
    try:
        id = request.matchdict['id']
        article = DBSession.query(Article).filter_by(id=id).first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    if article is None:
        return HTTPNotFound('No such page')

    if not 'slug' in request.matchdict or request.matchdict['slug'] != slugify(article.title):
        return HTTPFound(location=request.route_url('view_article_slug', id=article.id, slug=slugify(article.title)))

    formatted = format_article_metadata(article)
    formatted['body'] = markdown(article.body, extensions=['extra', 'headerid(level=2, forceid=False)'])
    formatted['edit_url'] = request.route_url('edit_article', id=id)
    return formatted
