from pyramid.config import Configurator

from pyramid.authentication import AuthTktAuthenticationPolicy, RemoteUserAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .security import groupfinder

from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings, root_factory='.models.RootFactory')

    # This mess is used to bypass authentication during testing.
    # Some day this will be cleaned up.
    if 'RemoteUserAuthenticationPolicy' in settings:
        authn_policy = RemoteUserAuthenticationPolicy(callback=groupfinder)
        authz_policy = ACLAuthorizationPolicy()
        config.set_authorization_policy(authz_policy)
    else:
        config.include("pyramid_persona")
        authn_policy = AuthTktAuthenticationPolicy(
            settings['persona.secret'], callback=groupfinder, hashalg='sha512')
    config.set_authentication_policy(authn_policy)

    if 'disable_caching' in settings and settings['disable_caching'] == 'true':
        config.add_static_view('static', 'static', cache_max_age=0)
    else:
        config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('add_article', '/add')
    config.add_route('edit_article', '/edit/{id}')
    config.add_route('atom_feed', '/feed.atom')
    config.add_route('view_article', '/{year}/{month}/{day}/{slug}')
    config.add_route('view_page', '/{slug}')
    config.add_route('view_all', '/')
    config.scan()
    return config.make_wsgi_app()
