from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings, set_cache_regions_from_settings

from pp.common.db import dbsetup

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # Database setup
    dbsetup.setup(dbsetup.modules_from_config(settings, 'commondb.'))
    dbsetup.init_from_config(settings, 'sqlalchemy.')

    # Session handling
    set_cache_regions_from_settings(settings)
    session_factory = session_factory_from_settings(settings)

    # TODO: not sure where get_root comes from, docs aren't clear
    #config = Configurator(root_factory=get_root, settings=settings)
    config = Configurator(settings=settings)

    config.set_session_factory(session_factory)

    # Routes
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    


    config.scan()
    return config.make_wsgi_app()

