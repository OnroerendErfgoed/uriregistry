# -*- coding: utf-8 -*-

from uriregistry.models import Application
from pyramid_urireferencer.models import ApplicationResponse

from uriregistry.utils import query_application

class TestUtils:

    def test_get_application_response(self):
        uri = "http://id.erfgoed.net/foobar/2"
        app = Application(1, "app_name", "http://uri/app", "http://url/app")
        r = query_application(app, uri)
        assert isinstance(r, ApplicationResponse)
        assert r.uri == app.uri
        assert r.url == app.url
        assert r.title == app.title
        assert r.success == False
