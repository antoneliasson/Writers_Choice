from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Article,
    )

from markdown import markdown

@view_config(route_name='view_article', renderer='templates/view.pt')
def view_article(request):
    try:
        id = request.matchdict['id']
        article = DBSession.query(Article).filter_by(id=id).first()

        title = article.title
        body = markdown(article.body)
        published = article.published.strftime('%Y-%m-%d')

    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return  {'title' : title, 'body' : body, 'published' : published}

@view_config(route_name='view_all', renderer='templates/view_all.pt')
def view_all(request):
    try:
        articles = DBSession.query(Article)
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    compilation = list()
    for article in articles:
        current = dict()
        current['title'] = article.title
        current['body'] = markdown(article.body)
        current['published'] = article.published.strftime('%Y-%m-%d')
        compilation.append(current)

    return {'articles' : compilation}
    
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

