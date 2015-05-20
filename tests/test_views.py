# -*- coding: utf-8 -*-
import pytest

from pyramid import testing
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest

from pyramid_urireferencer.models import RegistryResponse


@pytest.fixture
def pyramid_request():
    return testing.DummyRequest()

class TestViews:

    def test_home(self, pyramid_request):
        from uriregistry.views import RegistryView
        v = RegistryView(pyramid_request)
        res = v.home()
        assert isinstance(res, Response)

    def test_get_references_no_uri(self, pyramid_request, uriregistry):
        pyramid_request.uri_registry = uriregistry
        from uriregistry.views import RegistryView
        v = RegistryView(pyramid_request)
        with pytest.raises(HTTPBadRequest):
            res = v.get_references()

    def test_get_references_uri(self, pyramid_request, uriregistry):
        pyramid_request.uri_registry = uriregistry
        pyramid_request.params = {'uri': 'http://id.erfgoed.net/foo/1'}
        from uriregistry.views import RegistryView
        v = RegistryView(pyramid_request)
        res = v.get_references()
        assert isinstance(res, RegistryResponse)
        assert res.count == 0
        assert not res.has_references
        assert not res.success
