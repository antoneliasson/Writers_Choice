from datetime import datetime

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from ..models import (
    DBSession,
    Article,
    )

from . import slugify

@view_config(route_name='add_article', renderer='writers_choice:templates/edit_article.pt', permission='edit')
def add_article(request):
    body = ''
    message = ''
    if 'save-article' in request.params:
        title = request.params['title'].strip()
        body = request.params['body']
        if title == '':
            message = 'Article not saved. Title cannot be empty.'
        else:
            if 'publish' in request.params:
                publish = True
                date = datetime.now()
            else:
                publish = False
                date = None
            article = Article(title, body, is_published=publish, date_published=date)
            DBSession.add(article)
            # let the DB fill in the id
            DBSession.flush()

            return HTTPFound(location=request.route_url('edit_article', id=article.id))
    elif 'cancel-editing' in request.params:
        return HTTPFound(location=request.route_url('view_all'))

    page_title = 'New article — {}'.format(request.registry.settings['site_name'])
    submit_url = request.route_url('add_article')
    return {'title' : '', 'body' : body, 'submit_url' : submit_url, 'message' : message, 'page_title' : page_title, 'publish' : False}
