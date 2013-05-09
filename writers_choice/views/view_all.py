import markdown

from pyramid.view import view_config
from pyramid.security import has_permission

from sqlalchemy.exc import DBAPIError

from ..models import (
    DBSession,
    Article,
    )

from . import format_article_metadata, slugify

@view_config(route_name='view_all', renderer='writers_choice:templates/view_all.pt', permission='view')
def view_all(request):
    try:
        articles = DBSession.query(Article).order_by(Article.published.desc())
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    compilation = list()
    for article in articles:
        formatted = format_article_metadata(article)
        formatted['body'] = markdown.markdown(article.body, extensions=['extra', 'headerid(level=3, forceid=False)'])
        formatted['url'] = request.route_url('view_article_slug', id=article.id, slug=slugify(article.title))
        compilation.append(formatted)

    return {'articles' : compilation, 'user_can_edit' : has_permission('edit', request.context, request)}
