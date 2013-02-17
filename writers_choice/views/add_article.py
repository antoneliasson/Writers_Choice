from pyramid.view import view_config

from ..models import (
    DBSession,
    Article,
    )

@view_config(route_name='add_article', renderer='writers_choice:templates/edit_article.pt')
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

    submit_url = request.route_url('add_article')
    return {'title' : '', 'body' : '', 'submit_url' : submit_url}
