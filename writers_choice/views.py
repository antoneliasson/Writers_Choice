from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Article,
    )

def format_article(article):
    from markdown import markdown

    title = article.title
    body = markdown(article.body)
    published = article.published.strftime('%Y-%m-%d')

    return {'title' : title, 'body' : body, 'published' : published}

@view_config(route_name='view_article', renderer='templates/view_article.pt')
def view_article(request):
    try:
        id = request.matchdict['id']
        article = DBSession.query(Article).filter_by(id=id).first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    formatted = format_article(article)
    return formatted

@view_config(route_name='view_all', renderer='templates/view_all.pt')
def view_all(request):
    try:
        articles = DBSession.query(Article)
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    compilation = list()
    for article in articles:
        formatted = format_article(article)
        compilation.append(formatted)

    return {'articles' : compilation}

@view_config(route_name='add_article', renderer='templates/add_article.pt')
def add_article(request):
    if 'title' in request.params:
        from datetime import datetime
        from pyramid.httpexceptions import HTTPFound

        title = request.params['title']
        body = request.params['body']
        published = datetime.now()
        article = Article(title, body, published)
        DBSession.add(article)
        # let the DB fill in the id
        DBSession.flush()

        return HTTPFound(location = request.route_url('view_article', id=article.id))
    return {}

@view_config(route_name='edit_article', renderer='templates/edit_article.pt')
def edit_article(request):
    id = request.matchdict['id']
    article = DBSession.query(Article).filter_by(id=id).one()

    if 'title' in request.params:
        from pyramid.httpexceptions import HTTPFound
        title = request.params['title']
        body = request.params['body']
        article.title = title
        article.body = body
        DBSession.add(article)

        return HTTPFound(location = request.route_url('view_article', id=article.id))

    submit_url = request.route_url('edit_article', id=id)
    return {'title' : article.title, 'body' : article.body, 'submit_url' : submit_url}

conn_err_msg = """\
(Tabellen finns inte)

Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_Writers_Choice_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

