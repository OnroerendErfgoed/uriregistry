import requests

from pyramid.response import Response
from pyramid.view import view_config

from pyramid_urireferencer.models import (
    ApplicationResponse,
    RegistryResponse
)

from .utils import _stripped, _get_base_uri, _eq, query_application

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
        uri = self.request.params.get('uri', None)
        return _handle_uri(request.uri_registry, uri)

    @view_config(route_name='home', request_method='GET')
    def home(self):
        return Response(service_info, content_type='text/plain', status_int=200)


service_info = """Registryservice: what are my uri's up to?"""


def _handle_uri(uri_registry, uri):
    """
    This method takes the uri and checks the configuration if the base uri is used in other applications.
    A :class: RegistryResponse is returned with all the information
    :param uri: uri to be evaluated for references
    :return: :class: RegistryResponse
    """
    uri = _stripped(uri)
    base_uri = _get_base_uri(uri)
    #get applications that use the base_uri
    applications_list = []
    [applications_list.extend(u.applications) for u in uri_registry.uris if _eq(u.base_uri, base_uri)]
    #get distinct application list
    applications_list = list(set(applications_list))
    application_responses = [query_application(app, uri) for app in applications_list]

    return _get_registry_response(application_responses, uri, base_uri)

def _get_registry_response(application_responses, uri, base_uri):
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
    return RegistryResponse(uri, base_uri, success, has_references, count, application_responses)
