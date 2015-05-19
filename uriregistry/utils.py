# -*- coding: utf-8 -*-

import logging
log = logging.getLogger(__name__)

from pyramid_urireferencer.models import ApplicationResponse

def query_application(app, uri):
    """
    Checks if a certain app has references to a URI.

    :param uriregistry.models.Application: The application to be evaluated
    :param uri: The uri that has to be checked
    :rtype pyramid_urireferencer.models.ApplicationResponse:
    """
    try:
        url = _stripped(app.url) + '/references?uri=' + uri
        r = requests.get(url)
        a = ApplicationResponse.load_from_json(r.json())
        #todo app-metadata is added here to the response. Is there a possibility that the applicationresponse already has this metadata?
        a.name = app.name
        a.uri = app.uri
        a.url = app.url
        return a
    except:
        log.error('Could not check if uri %s is known to app %s (uri: %s)' % (uri, app.name, app.uri))
        return ApplicationResponse(app.name, app.uri, app.url, False, None, None, None)

def _stripped(uri):
    """
    Returns a stripped version of a string.
    All slashes (backward and forward) are replaced by forward-slashes.
    All leading and ending slashes and spaces are removed.
    :param uri: The string that has to be stripped
    :return: The stripped string
    """
    uri = uri.replace("\\", "/")
    return uri.strip('\ /')

def _get_base_uri(uri):
    """
    Returns the base uri when a uri (with identifier) is given
    :param uri: input uri (string) (with identifier)
    :return: base uri (string)
    """
    uri = _stripped(uri)
    return uri.rsplit("/", 1)[0]


def _eq (a, b):
    """
    Checks if 2 strings are identical after they are stripped
    :param a: string 1
    :param b: string 2
    :return: True if they are identical, otherwise False
    """
    if _stripped(a) == _stripped(b):
        return True
    return False
