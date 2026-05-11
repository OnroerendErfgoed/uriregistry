import json

import httpretty
import pytest
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

    @pytest.fixture
    def http_mock(self):
        httpretty.enable(allow_net_connect=False)
        yield httpretty
        httpretty.disable()
        httpretty.reset()

    def test_query_application_success(self, http_mock):
        app = Application(
            "http://uri/app", "app_name", "http://url/app/references"
        )
        payload = {
            "query_uri": "http://id.erfgoed.net/foobar/2",
            "title": app.title,
            "uri": app.uri,
            "service_url": app.service_url,
            "success": True,
            "has_references": True,
            "count": 4,
            "items": [],
        }
        http_mock.register_uri(
            http_mock.GET, app.service_url, body=json.dumps(payload)
        )
        r = query_application(app, "http://id.erfgoed.net/foobar/2")
        assert isinstance(r, ApplicationResponse)
        assert r.success is True
        assert r.has_references is True
        assert r.count == 4
