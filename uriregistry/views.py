import logging
from concurrent.futures import ThreadPoolExecutor

from pyramid.httpexceptions import HTTPBadRequest
from pyramid.response import Response
from pyramid.view import view_config
from pyramid_urireferencer.models import RegistryResponse

from .utils import query_application

log = logging.getLogger(__name__)


class ApplicationView:
    def __init__(self, request):
        self.request = request


class RestView(ApplicationView):
    pass


class RegistryView(RestView):

    @view_config(route_name="references", renderer="json", accept="application/json")
    def get_references(self):
        """
        Collect the references for a URI and relay them to the client.
        """
        uri = self.request.params.get("uri", None)
        if not uri:
            raise HTTPBadRequest("Please include a URI parameter.")

        applications = self.request.uri_registry.get_applications(uri)
        if not applications:
            return _get_registry_response([], uri)
        with ThreadPoolExecutor(max_workers=len(applications)) as tpe:
            futures = [tpe.submit(query_application, app, uri) for app in applications]
            application_responses = [future.result(timeout=25) for future in futures]

        return _get_registry_response(application_responses, uri)

    @view_config(route_name="home", request_method="GET")
    def home(self):
        """
        The root information page
        """
        return Response(service_info, content_type="text/plain", status_int=200)


service_info = """UriRegistry: what are my uri's up to?"""


def _get_registry_response(application_responses, uri):
    """
    Generate the final response by aggregating all the application responses.

    :param list application_responses:  All ApplicationResponse instances.
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
    return RegistryResponse(uri, success, has_references, count, application_responses)
