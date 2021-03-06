# -*- coding: utf-8 -*-
"""
Web helper functions.

"""
import logging
#import pprint

from pyramid.httpexceptions import HTTPFound, HTTPUnauthorized
from repoze.what import predicates


def get_log(extra=None):
    m = "{}.{}".format(__name__, extra) if extra else __name__
    return logging.getLogger(m)


def redirect(url):
    """Redirect user to the given URL"""
    raise HTTPFound(url)


def check_predicate(request, p):
    """
    Check a repoze predicate against a particular request
    """
    try:
        get_log().info("Checking pred %r" % p)
        #get_log().info(pprint.pformat(request.environ))
        p.check_authorization(request.environ)
    except predicates.NotAuthorizedError:
        raise HTTPUnauthorized


def login_required(request_handler):
    """A decorator used to require a user to be logged in before
    access a view.

    This is used with view_config as follows::

        @view_config(
            decorator=login_required,
            route_name='survey', request_method='GET',
            accept="text/html", renderer='home.jinja2',
        )
        def something(request):
            :
            etc

    """
    log = get_log('login_required')

    def _fn(context, request):
        try:
            log.info("checking / requiring login")
            p = predicates.not_anonymous(msg='Must be logged in')
            p.check_authorization(request.environ)

        except predicates.NotAuthorizedError:
            log.debug("login required.")
            redirect('/login?came_from={}'.format(request.path))

        else:
            log.debug("logged in.")

        return request_handler(request)

    return _fn
