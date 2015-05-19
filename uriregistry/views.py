import requests

from pyramid.response import Response
from pyramid.view import view_config

from pyramid_urireferencer.models import (
    ApplicationResponse,
    RegistryResponse
)

from .utils import query_application

import logging
log = logging.getLogger(__name__)


class ApplicatieView(object):
    def __init__(self, request):
        self.request = request

class RestView(ApplicatieView):
    pass

class RegistryView(RestView):

    @view_config(route_name='references', renderer='json', accept='application/json')
    def get_references(self):
        uri = self.request.params.get('uri', '')

        applications = self.request.uri_registry.get_applications(uri)
        application_responses = [query_application(app, uri) for app in applications]

        return _get_registry_response(application_responses, uri)

    @view_config(route_name='home', request_method='GET')
    def home(self):
        return Response(service_info, content_type='text/plain', status_int=200)


service_info = """Registryservice: what are my uri's up to?"""


def _get_registry_response(application_responses, uri):
    """
    :param list application_responses:  All :class:`pyramid_urireferencer.models.ApplicationResponse` instances.
    :param str uri: Uri that was evaluated
    :param str base_uri: Base uri of the uri that was evaluated
    :return: :class:`pyramid_urireferencer.models.RegistryResponse` with all \
        information the registry has collected
    """
    success = True
    has_references = False
    count = 0
    for r in application_responses:
        if not r.success:
            success = False
        if r.has_references:
            has_references = True
        if r.count is not None:
            count = count + r.count
    return RegistryResponse(uri, uri, success, has_references, count, application_responses)
