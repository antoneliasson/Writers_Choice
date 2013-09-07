from markdown import markdown

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound

from sqlalchemy.orm.exc import NoResultFound

from writers_choice.models import DBSession, Page

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

    from .view_all import get_navigation
    navigation = get_navigation(request)

    return {'content' : content, 'user_can_edit' : False, 'navigation' : navigation}
