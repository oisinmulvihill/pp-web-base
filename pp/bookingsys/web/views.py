import logging
import pprint

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPUnauthorized
from repoze.what import predicates

def get_log():
    return logging.getLogger('pp.bookingsys.web.views')

def redirect(url):
    """Redirect user to the given URL"""
    raise HTTPFound(url)

def check_predicate(request, p):
    try:
        get_log().info("Checking pred %r" % p)
        get_log().info(pprint.pformat(request.environ))
        p.check_authorization(request.environ)
    except predicates.NotAuthorizedError:
        raise HTTPUnauthorized


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def home(request):
    return {'project': 'pp.bookingsys.web'}



@view_config(route_name='protected', renderer='templates/protected.jinja2')
def protected(request):
    get_log().info("protected")
    check_predicate(request, predicates.not_anonymous(msg='Must be logged in'))
    return {}


@view_config(route_name='login', renderer='templates/login.jinja2')
def login(request):
    """Start the user login."""
    came_from = request.GET.get('came_from')
    get_log().info("login: came from %r" % came_from)
    if not came_from:
        came_from = request.route_url('home')

    login_handler = request.registry.settings['pp.auth.login_handler_url']
    get_log().info("login handler: %r " % login_handler)
    return dict(page='login', 
                came_from=came_from,
                login_handler=login_handler)

    #login_counter = request.environ['repoze.who.logins']

    #if login_counter > 0:
    #    request.session.flash('Wrong credentials')

    #return dict(page='login', 
    #            login_counter=str(login_counter),
    #            came_from=came_from)


#@view_config(route_name='login_handler', renderer='templates/login.jinja2')
#def login_handler(request):
#    """
#    Redirect the user to the initially requested page on successful
#    authentication or redirect her back to the login page if login failed.
#
#    """
#    raise ValueError
#    came_from = request.matchdict.get('came_from')
#    if not came_from:
#        came_from = request.route_url('home')
#
#    get_log().info("login_handler: came from %r, identity=%r" % (came_from, request.identity))
#
#    if not request.identity:
#        login_counter = request.environ['repoze.who.logins'] + 1
#        redirect('/login',
#            params=dict(came_from=came_from, __logins=login_counter))
#    userid = request.identity['repoze.who.userid']
#    request.session.flash('Welcome back, %s!' % userid)
#    redirect(came_from)

#@expose()
#def post_logout(self, came_from=lurl('/')):
#    """
#    Redirect the user to the initially requested page on logout and say
#    goodbye as well.
#
#    """
#    flash(_('We hope to see you soon!'))
#    redirect(came_from)
