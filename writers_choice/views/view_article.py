from markdown import markdown

from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import (
    DBSession,
    Article,
    )

from . import format_article_metadata

@view_config(route_name='view_article', renderer='writers_choice:templates/view_article.pt')
@view_config(route_name='view_article_slug', renderer='writers_choice:templates/view_article.pt')
def view_article(request):
    try:
        id = request.matchdict['id']
        article = DBSession.query(Article).filter_by(id=id).first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    formatted = format_article_metadata(article)
    formatted['body'] = markdown(article.body, extensions=['extra', 'headerid(level=2, forceid=False)'])
    formatted['edit_url'] = request.route_url('edit_article', id=id)
    return formatted
