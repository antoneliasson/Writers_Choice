from datetime import datetime, timedelta

from markdown import markdown

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import has_permission

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm.exc import NoResultFound

from ..models import (
    DBSession,
    Article,
    )

from . import format_article_metadata, slugify

@view_config(route_name='view_article', renderer='writers_choice:templates/view_article.pt', permission='view')
def view_article(request):
    try:
        d = datetime(int(request.matchdict['year']),
                     int(request.matchdict['month']),
                     int(request.matchdict['day']))
        slug = request.matchdict['slug']
        article = DBSession.query(Article).filter(
            Article.is_published==True,
            d <= Article.date_published,
            Article.date_published < d+timedelta(days=1),
            Article.slug==slug).one()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    except NoResultFound:
        return HTTPNotFound('No such article.')

    formatted = format_article_metadata(article)
    formatted['body'] = markdown(article.body, extensions=['extra', 'headerid(level=2, forceid=False)'])
    formatted['edit_url'] = request.route_url('edit_article', id=article.id)

    from .view_all import get_navigation
    navigation = get_navigation(request)

    return {'content' : formatted, 'user_can_edit' : has_permission('edit', request.context, request), 'navigation' : navigation}
