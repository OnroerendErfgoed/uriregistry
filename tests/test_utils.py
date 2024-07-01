from pyramid_urireferencer.models import ApplicationResponse

from uriregistry.models import Application
from uriregistry.utils import query_application


class TestUtils:

    def test_get_application_response(self):
        uri = "http://id.erfgoed.net/foobar/2"
        app = Application(
            "http://www.app.net", "app_name", "http://www.app.net/references"
        )
        r = query_application(app, uri)
        assert isinstance(r, ApplicationResponse)
        assert r.uri == app.uri
        assert r.service_url == app.service_url
        assert r.title == app.title
        assert r.success is False
