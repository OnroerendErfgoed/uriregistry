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
        url = app.url + '/references?uri=' + uri
        r = requests.get(url)
        a = ApplicationResponse.load_from_json(r.json())
        #todo app-metadata is added here to the response. Is there a possibility that the applicationresponse already has this metadata?
        a.title = app.title
        a.uri = app.uri
        a.url = app.url
        return a
    except:
        log.error('Could not check if uri %s is known to app %s (uri: %s)' % (uri, app.title, app.uri))
        return ApplicationResponse(app.title, app.uri, app.url, False, None, None, None)
