import logging

import requests
from pyramid_urireferencer.models import ApplicationResponse

log = logging.getLogger(__name__)


def query_application(app, uri):
    """
    Checks if a certain app has references to a URI.

    :param uriregistry.models.Application: The application to be evaluated
    :param uri: The uri that has to be checked
    :rtype pyramid_urireferencer.models.ApplicationResponse:
    """
    try:
        r = requests.get(app.service_url, params={"uri": uri})
        a = ApplicationResponse.load_from_json(r.json())
        return a
    except Exception:
        log.error(
            f"Could not check if uri {uri} is known to app {app.title} (uri: {app.uri})"
        )
        return ApplicationResponse(
            app.title, app.uri, app.service_url, False, None, None, None
        )
