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
        url = '{0}?{1}'.format(app.service_url, urllib.urlencode({'uri': uri}))
        r = requests.get(url)
        a = ApplicationResponse.load_from_json(r.json())
        return a
    except:
        log.error('Could not check if uri %s is known to app %s (uri: %s)' % (uri, app.title, app.uri))
        return ApplicationResponse(app.title, app.uri, app.service_url, False, None, None, None)
