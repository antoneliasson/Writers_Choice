import markdown

from pyramid.view import view_config
from pyramid.security import has_permission

from sqlalchemy.exc import DBAPIError

from ..models import (
    DBSession,
    Article,
    Page
)

from . import format_article_metadata, slugify

@view_config(route_name='view_all', renderer='writers_choice:templates/view_all.pt', permission='view')
def view_all(request):
    try:
        articles = DBSession.query(Article).order_by(Article.date_published.desc()).filter_by(is_published=True)
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    compilation = list()
    for article in articles:
        formatted = format_article_metadata(article)
        formatted['body'] = markdown.markdown(article.body, extensions=['extra', 'headerid(level=3, forceid=False)'])
        year, month, day = article.date_published.timetuple()[:3]
        formatted['url'] = request.route_url('view_article',
                                             year=year,
                                             month=month,
                                             day=day,
                                             slug=slugify(article.title))
        compilation.append(formatted)

    navigation = get_navigation(request)

    return {'articles' : compilation, 'user_can_edit' : has_permission('edit', request.context, request), 'navigation' : navigation}

def get_navigation(request):
    pages = DBSession.query(Page).order_by(Page.title)

    tabs = list()
    home = {'title' : 'Home', 'url' : request.route_url('view_all')}
    tabs.append(home)
    for page in pages:
        tab = {'title' : page.title, 'url' : request.route_url('view_page', slug=page.slug)}
        tabs.append(tab)
    return tabs
