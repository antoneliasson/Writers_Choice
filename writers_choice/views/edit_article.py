from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm.exc import NoResultFound

from ..models import (
    DBSession,
    Article,
    )

from . import slugify

@view_config(route_name='edit_article', renderer='writers_choice:templates/edit_article.pt', permission='edit')
def edit_article(request):
    id = request.matchdict['id']
    try:
        article = DBSession.query(Article).filter_by(id=id).one()
    except NoResultFound:
        return HTTPNotFound('Article not found')

    message = ''
    body = article.body
    if 'save-article' in request.params:
        title = request.params['title'].strip()
        body = request.params['body']
        if title == '':
            message = 'Article not saved. Title cannot be empty.'
        else:
            article.title = title
            article.body = body
            DBSession.add(article)

            return HTTPFound(location=request.route_url('view_article_slug', id=article.id, slug=slugify(article.title)))
    elif 'cancel-editing' in request.params:
        return HTTPFound(location=request.route_url('view_article_slug', id=article.id, slug=slugify(article.title)))

    page_title = 'Editing {} — {}'.format(article.title, request.registry.settings['site_name'])
    submit_url = request.route_url('edit_article', id=id)
    return {'title' : article.title, 'body' : body, 'submit_url' : submit_url, 'message' : message, 'page_title' : page_title}
