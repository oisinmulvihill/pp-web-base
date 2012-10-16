import logging

from pyramid.config import Configurator

from pp.common.db import dbsetup
from pp.auth.middleware import add_auth_from_config


def get_log():
    return logging.getLogger('pp.web.base')


def load_prefix_includes(config, settings):
    """
    Loads pyramid modules from the config much like
    pyramid.includes, with added support for route prefix
    Config format is::
        [app:main]
        pyramid.route_includes =
            <module>, <prefix>
    """
    for line in [l for l in settings.get('pyramid.route_includes', '').split('\n') if l]:
        mod, prefix = [i.strip() for i in line.split(',')]
        get_log().info("Loading module %r with route prefix %r" % (mod, prefix))
        # '/' is the same as no prefix at all, but useful to denote the  root module
        # in the config file
        if prefix == '/':
            prefix = None
        config.include(mod, route_prefix=prefix)


def common_db_configure(settings, use_transaction=True):
    """Configure common db using the given pyramid settings.

    This will use 'commondb.' and 'sqlalchemy.' in the configuration.

    :returns: None

    """
    dbsetup.setup(dbsetup.modules_from_config(settings, 'commondb.'))
    dbsetup.init_from_config(settings, 'sqlalchemy.', use_transaction=use_transaction)


def pp_auth_middleware(settings, app):
    """Configure the pp auth packages using the given pyramid settings.

    This will use 'pp.auth.' in the configuration.

    :returns: The given app wrapped in configured pp auth middleware.

    """
    return add_auth_from_config(app, settings, 'pp.auth.')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # Database setup
    common_db_configure(settings)

    # Add some default settings (would be nicer to do this programatically)
    settings['jinja2.filters'] = "route_url = pyramid_jinja2.filters:route_url_filter"

    # Load config file - this will initiate all the includes set there
    # from pyramid.includes
    config = Configurator(settings=settings)

    # Common Routes and Views
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('ping', '/ping')

    # This scans everything under this package for view decorated methods to
    # match up with the routes
    config.scan()

    # Load includes with route prefixes
    load_prefix_includes(config, settings)

    # Add base templates dir to the search path. This has to go last so other
    # projects have a chance to add their templates to the search path first.
    config.add_jinja2_search_path("%s:templates" % __name__)

    app = config.make_wsgi_app()

    app = pp_auth_middleware(settings, app)

    return app
