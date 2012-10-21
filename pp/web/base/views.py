# -*- coding: utf-8 -*-
"""
"""
import logging
import datetime

from pyramid.view import view_config
import pyramid.httpexceptions
from repoze.what import predicates

from util import check_predicate


def get_log():
    return logging.getLogger('pp.web.base.views')


@view_config(route_name='ping', renderer='ping.jinja2')
def ping(request):
    return {'ping': datetime.datetime.now()}


@view_config(route_name='login', renderer='login.jinja2')
def login(request):
    """Start the user login."""
    came_from = request.GET.get('came_from')
    get_log().info("login: came from %r" % came_from)
    if not came_from:
        came_from = '/'

    login_handler = request.registry.settings['pp.auth.login_handler_url']
    get_log().info("login handler: %r " % login_handler)
    return dict(page='login',
                came_from=came_from,
                login_handler=login_handler)


@view_config(route_name='logout', renderer='login.jinja2')
def logout(request):
    """Log out the user."""
    get_log().info("logout")
    check_predicate(request, predicates.not_anonymous(msg='Must be logged in'))
    cookie = request.environ['repoze.who.plugins']['cookie']
    headers = cookie.forget(request.environ, None)
    # TODO: read logout URL from config? 
    raise pyramid.httpexceptions.HTTPFound("/", headers=headers)


# This login handler is implemented by the WSGI middleware

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
