from datetime import datetime, timedelta

from markdown import markdown
from markdown.extensions import headerid

from pyramid.view import view_config
from pyramid.security import has_permission
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm.exc import NoResultFound

from writers_choice.models import (
    DBSession,
    Article,
    Page
)

def format_article_metadata(article):
    id = article.id
    title = article.title
    published = article.date_published.strftime('%Y-%m-%d')

    return {'id' : id, 'title' : title, 'published' : published}

@view_config(route_name='view_all', renderer='writers_choice:templates/view_all.pt', permission='view')
def view_all(request):
    try:
        articles = DBSession.query(Article).order_by(Article.date_published.desc()).filter_by(is_published=True)
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    compilation = list()
    for article in articles:
        formatted = format_article_metadata(article)
        formatted['body'] = markdown(article.body, extensions=['extra', 'headerid(level=3, forceid=False)'])
        year, month, day = article.date_published.timetuple()[:3]
        formatted['url'] = request.route_url('view_article',
                                             year=year,
                                             month=month,
                                             day=day,
                                             slug=article.slug)
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

    navigation = get_navigation(request)

    return {'content' : formatted, 'user_can_edit' : has_permission('edit', request.context, request), 'navigation' : navigation}

@view_config(route_name='view_page', renderer='writers_choice:templates/view_article.pt', permission='view')
def view_page(request):
    slug = request.matchdict['slug']
    try:
        page = DBSession.query(Page).filter_by(slug=slug).one()
    except NoResultFound:
        return HTTPNotFound('Page not found')

    content = {'id' : page.id, 'title' : page.title}
    content['body'] = markdown(page.body, extensions=['extra', 'headerid(level=2, forceid=False)'])
    content['edit_url'] = ''

    navigation = get_navigation(request)

    return {'content' : content, 'user_can_edit' : False, 'navigation' : navigation}
