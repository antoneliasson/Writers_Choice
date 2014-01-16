from datetime import datetime, timedelta

from markdown import markdown
from markdown.extensions import headerid

from pyramid.view import view_config
from pyramid.security import has_permission
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.response import Response

from sqlalchemy.orm.exc import NoResultFound

from pyatom import AtomFeed

from writers_choice.models import (
    DBSession,
    Article,
    Page
)

def format_article(article, is_sole_article):
    title = article.title
    published = article.date_published.strftime('%Y-%m-%d')
    headerlevel = 2 if is_sole_article else 3
    body = markdown(article.body, extensions=['extra', 'headerid(level={}, forceid=False)'.format(headerlevel)])

    return {
        'title' : title,
        'published' : published,
        'body' : body
    }

def get_navigation(request):
    pages = DBSession.query(Page).order_by(Page.title)

    tabs = list()
    home = {'title' : 'Home', 'url' : request.route_url('view_all')}
    tabs.append(home)
    for page in pages:
        tab = {'title' : page.title,
               'url' : request.route_url('view_page', slug=page.slug)}
        tabs.append(tab)
    return tabs

@view_config(route_name='view_all',
             renderer='writers_choice:templates/view_all.pt',
             permission='view')
def view_all(request):
    articles = DBSession.query(Article).order_by(
        Article.date_published.desc()).filter_by(is_published=True)

    compilation = list()
    for article in articles:
        content = format_article(article, True)
        year, month, day = article.date_published.timetuple()[:3]
        content['url'] = request.route_url('view_article',
                                           year=year,
                                           month=month,
                                           day=day,
                                           slug=article.slug)
        compilation.append(content)

    return {
        'articles' : compilation,
        'user_can_edit' : has_permission('edit', request.context, request),
        'navigation' : get_navigation(request)
    }

@view_config(route_name='view_article',
             renderer='writers_choice:templates/view_article.pt',
             permission='view')
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
    except NoResultFound:
        return HTTPNotFound('No such article.')

    content = format_article(article, True)
    content['edit_url'] = request.route_url('edit_article', id=article.id)

    return {
        'content' : content,
        'user_can_edit' : has_permission('edit', request.context, request),
        'navigation' : get_navigation(request)
    }

@view_config(route_name='view_page',
             renderer='writers_choice:templates/view_article.pt',
             permission='view')
def view_page(request):
    slug = request.matchdict['slug']
    try:
        page = DBSession.query(Page).filter_by(slug=slug).one()
    except NoResultFound:
        return HTTPNotFound('Page not found')

    content = {
        'title' : page.title,
        'body' : markdown(page.body, extensions=['extra', 'headerid(level=2, forceid=False)']),
        'edit_url' : '' # not implemented yet
    }

    return {
        'content' : content,
        'user_can_edit' : False,
        'navigation' : get_navigation(request)
    }

@view_config(route_name='atom_feed', permission='view')
def atom_feed(request):
    feed = AtomFeed(
        title=request.registry.settings['site_name'],
        feed_url=request.route_url('atom_feed'),
        url=request.route_url('view_all'),
        author=request.registry.settings['site_name'] # will do for now
    )

    articles = DBSession.query(Article).order_by(
        Article.date_published.desc()).filter_by(is_published=True) # TODO: limit x
    for article in articles:
        content = format_article(article, True)
        year, month, day = article.date_published.timetuple()[:3]
        feed.add(
            content['title'],
            content['body'],
            url=request.route_url('view_article',
                                  year=year,
                                  month=month,
                                  day=day,
                                  slug=article.slug),
            updated=article.updated,
            published=article.date_published
        )

    return Response(
        body=feed.to_string(),
        content_type='application/atom+xml',
    )
