from markdown import markdown

from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import (
    DBSession,
    Article,
    )

from . import format_article_metadata

@view_config(route_name='view_all', renderer='writers_choice:templates/view_all.pt')
def view_all(request):
    try:
        articles = DBSession.query(Article).order_by(Article.published.desc())
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    compilation = list()
    for article in articles:
        formatted = format_article_metadata(article)
        formatted['body'] = markdown(article.body, extensions=['headerid(level=3, forceid=False)'])
        compilation.append(formatted)

    return {'articles' : compilation}
