import logging

from pyramid.config import Configurator
from pyramid.renderers import JSON
from pp.db import dbsetup
from pp.auth.middleware import add_auth_from_config
from pp.utils.json_ import CustomEncoder, get_adapters


def get_log(e=None):
    return logging.getLogger("{0}.{1}".format(__name__, e) if e else __name__)


def load_prefix_includes(config, settings):
    """
    Loads pyramid modules from the config much like
    pyramid.includes, with added support for route prefix
    Config format is::
        [app:main]
        pyramid.route_includes =
            <module>, <prefix>
    """
    lines = [
        l for l in settings.get('pyramid.route_includes', '').split('\n') if l
    ]
    for line in lines:
        mod, prefix = [i.strip() for i in line.split(',')]
        get_log().info(
            "Loading module %r with route prefix %r" % (mod, prefix)
        )
        # '/' is the same as no prefix at all, but useful to denote the root
        # module in the config file
        if prefix == '/':
            prefix = None
        config.include(mod, route_prefix=prefix)


def common_db_configure(settings, use_transaction=True):
    """Configure common db using the given pyramid settings.

    This will use 'commondb.' and 'sqlalchemy.' in the configuration.

    :returns: None

    """
    if 'sqlalchemy' not in settings:
        get_log().warn(
            "common_db_configure: sqlalchemy not present disabling."
        )

    else:
        dbsetup.setup(dbsetup.modules_from_config(settings, 'commondb.'))
        dbsetup.init_from_config(
            settings, 'sqlalchemy.', use_transaction=use_transaction
        )


def pp_auth_middleware(settings, app):
    """Configure the pp auth packages using the given pyramid settings.

    This will use 'pp.auth.' in the configuration.

    :returns: The given app wrapped in configured pp auth middleware.

    """
    return add_auth_from_config(app, settings, 'pp.auth.')


def pp_api_access_token_middleware(settings, app):
    """Set up API Access token authentication.

    :param settings:

    :param app:

    """
    log = get_log('pp_api_access_token_middleware')

    try:
        from pp.user.client import rest

    except ImportError:
        log.warn(
            'pp-user-client not found. Disabling api access token middleware.'
        )
        return app

    from pp.apiaccesstoken.middleware import ValidateAccessToken

    uri = settings.get('pp.user.uri')
    if not uri:
        raise ValueError(
            "pp.user.uri is not set in the configuration!"
        )

    user_svc = rest.UserService(uri)
    secret_for_access_token = user_svc.user.secret_for_access_token

    def recover_secret(access_token):
        """This needs to recover the access_secret for the given access_token.

        :returns: The access_secret or None if nothing was found.

        """
        return secret_for_access_token(access_token)

    log.info("API token lookup initialised and ready to roll.")

    return ValidateAccessToken(app, recover_secret=recover_secret)


def setup_json_adapters(config):
    """ Setup json rendering using our custom encoder
    """
    # Extract adapters from our common global json adapters, curry them to
    # include the request object
    adapters = []
    for type_, fn in get_adapters():
        def new_fn(obj, request):
            return fn(obj)
        adapters.append((type_, new_fn))

    json_renderer = JSON(cls=CustomEncoder, adapters=adapters)
    config.add_renderer('json', json_renderer)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # Database setup
    common_db_configure(settings)

    # Add some default settings (would be nicer to do this programatically)
    f = "route_url = pyramid_jinja2.filters:route_url_filter"
    settings['jinja2.filters'] = f

    # Load config file - this will initiate all the includes set there
    # from pyramid.includes
    config = Configurator(settings=settings)

    # Setup json adapters
    setup_json_adapters(config)

    # Common Routes and Views
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

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

    app = pp_api_access_token_middleware(settings, app)

    return app
