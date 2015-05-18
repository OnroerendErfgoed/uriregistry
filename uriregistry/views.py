import requests

from pyramid.response import Response
from pyramid.view import view_config

from uriregistry import get_urilist
from pyramid_urireferencer.models import (
    ApplicationResponse,
    RegistryResponse
)

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
        return _handle_uri(uri)

    @view_config(route_name='home', request_method='GET')
    def home(self):
        return Response(service_info, content_type='text/plain', status_int=200)


service_info = """Registryservice: service voor registratieafhandeling van uri's"""


def _handle_uri(uri):
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
    [applications_list.extend(u.applications) for u in get_urilist() if _eq(u.base_uri, base_uri)]
    #get distinct application list
    applications_list = list(set(applications_list))
    application_responses = [_get_application_response(app, uri) for app in applications_list]

    return _get_registry_response(application_responses, uri, base_uri)

def _get_registry_response(application_responses, uri, base_uri):
    """

    :param application_responses: Array with all :class: ApplicationResponse
    :param uri: uri that is evaluated for references
    :param base_uri: base uri (without identifier) of the uri (with identifier)
    :return: :class: RegistryResponse with all the references-information the registry has collected
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

def _get_application_response(app, uri):
    """
    This method returns an ApplicationResponse-object b
    :param app: The application that has to be evaluated if there are references to the uri
    :param uri: The uri that has to be checked
    :return: :class:`ApplicationResponse` with all the information of the response of the application
    """
    try:
        url = _stripped(app.url) + '/references?uri=' + uri
        #todo security (user/password) for request?
        #data = json.dumps({'name':'test', 'description':'some test repo'})
        #r = requests.get(url+'/references', data, auth=('user', '*****')
        r = requests.get(url)
        a = ApplicationResponse.load_from_json(r.json())
        #todo app-metadata is added here to the response. Is there a possibility that the applicationresponse already has this metadata?
        a.name = app.name
        a.uri = app.uri
        a.url = app.url
        return a
    except:
        return ApplicationResponse(app.name, app.uri, app.url, False, None, None, None)

def _get_base_uri(uri):
    """
    Returns the base uri when a uri (with identifier) is given
    :param uri: input uri (string) (with identifier)
    :return: base uri (string)
    """
    uri = _stripped(uri)
    return uri.rsplit("/", 1)[0]

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
