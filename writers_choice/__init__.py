from pyramid.config import Configurator

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .security import groupfinder

from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    authn_policy = AuthTktAuthenticationPolicy(
        'sosecret', callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings, root_factory='.models.RootFactory')

    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    # config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('static', 'static', cache_max_age=0)
    config.add_route('add_article', '/add')
    config.add_route('edit_article', '/edit/{id}')
    config.add_route('view_article_noslug', '/{id:\d+}')
    config.add_route('view_article_slug', '/{id:\d+}/{slug:.*}')
    config.add_route('view_all', '/')
    config.scan()
    return config.make_wsgi_app()
