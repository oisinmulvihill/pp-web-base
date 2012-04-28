import logging
import pprint

from pyramid.httpexceptions import HTTPFound, HTTPUnauthorized
from repoze.what import predicates


def get_log():
    return logging.getLogger('pp.web.base.util')


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
