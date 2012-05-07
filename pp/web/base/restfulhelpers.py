# -*- coding: utf-8 -*-
"""
Useful classes and methods to aid RESTful webservice development in Pyramid.

PythonPro Limited
2012-01-14

"""
import httplib
import logging
import traceback

from pyramid.request import Response

from pp.bookingsys.frontend.utils import status_body


def get_log():
    return logging.getLogger("pp.bookingsys.frontend")


def notfound_404_view(request):
    """A custom 404 view returning JSON error message body instead of HTML.

    :returns: a JSON response with the body::

        json.dumps(dict(error="URI Not Found '...'"))

    """
    msg = str(request.exception.message)
    get_log().info("notfound_404_view: URI '%s' not found!" % str(msg))
    request.response.status = httplib.NOT_FOUND
    request.response.content_type = "application/json"
    body = status_body(
        status="error",
        message="URI Not Found '%s'" % msg,
    )
    return Response(body)


def xyz_handler(status):
    """A custom xyz view returning JSON error message body instead of HTML.

    :returns: a JSON response with the body::

        json.dumps(dict(error="URI Not Found '...'"))

    """
    def handler(request):
        msg = str(request.exception.message)
        get_log().info("xyz_handler (%s): %s" % (status, str(msg)))
        request.response.status = status
        request.response.content_type = "application/json"
        body = status_body(
            status="error",
            message=msg,
        )
        return Response(body)

    return handler


# Reference:
#  * http://zhuoqiang.me/a/restful-pyramid
#
class HttpMethodOverrideMiddleware(object):
    '''WSGI middleware for overriding HTTP Request Method for RESTful support
    '''
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        if 'POST' == environ['REQUEST_METHOD']:
            override_method = ''

            # First check the "_method" form parameter
            if 'form-urlencoded' in environ['CONTENT_TYPE']:
                from webob import Request
                request = Request(environ)
                override_method = request.str_POST.get('_method', '').upper()

            # If not found, then look for "X-HTTP-Method-Override" header
            if not override_method:
                override_method = environ.get('HTTP_X_HTTP_METHOD_OVERRIDE', '').upper()

            if override_method in ('PUT', 'DELETE', 'OPTIONS', 'PATCH'):
                # Save the original HTTP method
                environ['http_method_override.original_method'] = environ['REQUEST_METHOD']
                # Override HTTP method
                environ['REQUEST_METHOD'] = override_method

        return self.application(environ, start_response)


class JSONErrorHandler(object):
    """Capture exceptions usefully and return to aid the client side.

    :returns: status_body set for an error.

    E.g.::

        status_body(
            status="error",
            message=exception string,
            traceback="long form of the traceback."
        )

    """
    def __init__(self, application):
        self.app = application

    def formatError(self):
        """Return a string representing the last traceback.
        """
        exception, instance, tb = traceback.sys.exc_info()
        error = "".join(traceback.format_tb(tb))
        return error

    def __call__(self, environ, start_response):
        try:
            return self.app(environ, start_response)
        except Exception, e:
            errmsg = "%d %s" % (
                httplib.INTERNAL_SERVER_ERROR,
                httplib.responses[httplib.INTERNAL_SERVER_ERROR]
            )
            start_response(errmsg, [('Content-Type', 'application/json')])
            return status_body(
                status="error",
                message="%s: %s" % (type(e).__name__, str(e)),
                # Should this be disabled on production?
                traceback=self.formatError()
            )



