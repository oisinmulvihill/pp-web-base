# -*- coding: utf-8 -*-
"""
Useful classes and methods to aid RESTful webservice development in Pyramid.

PythonPro Limited
2012-01-14

"""
import json
import httplib
import logging
import traceback

from pyramid.request import Response


def get_log(extra=None):
    m = "{}.{}".format(__name__, extra) if extra else __name__
    return logging.getLogger(m)


def status_body(status="ok", message="", error="", traceback="", to_json=True):
    """Create a JSON response body we will use for error and other situations.

    :param status: Default "ok" or "error".

    :param message: Default "" or given string.

    :param error: Default "" or given string like ValueError.

    :param traceback: Default "" or formatted traceback string.

    :param to_json: Default True, return a JSON string or dict is False.

    the to_json is used in situations where something else will take care
    of to JSON conversion.

    :returns: JSON status response body.

    The default response is::

        json.dumps(dict(
            status="ok",
            message="",
            traceback="",
        ))

    """
    body = dict(
        status=status,
        message=message,
        error=error,
        traceback=traceback,
    )

    if to_json:
        body = json.dumps(body)

    return body


def status_err(exc, tb):
    return status_body("error", str(exc), exc.__class__.__name__, to_json=False)


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
    log = get_log()

    def handler(request):
        msg = str(request.exception.message)
        log.info("xyz_handler (%s): %s" % (status, str(msg)))
        #request.response.status = status
        #request.response.content_type = "application/json"
        body = status_body(
            status="error",
            message=msg,
        )

        rc = Response(body)
        rc.status = status
        rc.content_type = "application/json"

        return rc

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
            # if 'form-urlencoded' in environ['CONTENT_TYPE']:
            #     from webob import Request
            #     request = Request(environ)
            #     override_method = request.str_POST.get('_method', '').upper()

            # If not found, then look for "X-HTTP-Method-Override" header
            if not override_method:
                override_method = environ.get(
                    'HTTP_X_HTTP_METHOD_OVERRIDE', ''
                ).upper()

            if override_method in ('PUT', 'DELETE', 'OPTIONS', 'PATCH'):
                # Save the original HTTP method
                method = environ['REQUEST_METHOD']
                environ['http_method_override.original_method'] = method
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
        self.log = get_log("JSONErrorHandler")

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
            self.log.exception("error: ")
            errmsg = "%d %s" % (
                httplib.INTERNAL_SERVER_ERROR,
                httplib.responses[httplib.INTERNAL_SERVER_ERROR]
            )
            start_response(errmsg, [('Content-Type', 'application/json')])

            message = str(e)
            error = "%s" % (type(e).__name__)
            self.log.error("%s: %s" % (error, message))

            return status_body(
                status="error",
                message=message,
                error=error,
                # Should this be disabled on production?
                traceback=self.formatError()
                #traceback="self.formatError()"
            )
