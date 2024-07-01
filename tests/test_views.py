import pytest
from pyramid import testing
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.response import Response
from pyramid_urireferencer.models import ApplicationResponse
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
            v.get_references()

    def test_get_references_uri(self, pyramid_request, uriregistry):
        pyramid_request.uri_registry = uriregistry
        pyramid_request.params = {"uri": "http://id.erfgoed.net/foo/1"}
        from uriregistry.views import RegistryView

        v = RegistryView(pyramid_request)
        res = v.get_references()
        assert isinstance(res, RegistryResponse)
        assert res.count == 0
        assert not res.has_references
        assert not res.success


def test_get_registry_response():
    from uriregistry.views import _get_registry_response

    uri = "http://id.erfgoed.net/foobar/2/"
    app_response_success_ref = ApplicationResponse(
        "app2_name", "http://uri/app2", "http://url/app2", True, True, 2, []
    )
    app_response_success_ref2 = ApplicationResponse(
        "app2_name", "http://uri/app2", "http://url/app2", True, True, 3, []
    )
    app_response_nosuccess = ApplicationResponse(
        "app2_name", "http://uri/app2", "http://url/app2", False, None, None, None
    )
    app_response_nosuccess2 = ApplicationResponse(
        "app2_name", "http://uri/app2", "http://url/app2", False, None, None, None
    )
    app_response_success_noref = ApplicationResponse(
        "app2_name", "http://uri/app2", "http://url/app2", True, False, None, None
    )
    app_response_success_noref2 = ApplicationResponse(
        "app2_name", "http://uri/app2", "http://url/app2", True, False, None, None
    )

    r = _get_registry_response(
        [app_response_success_ref, app_response_success_ref2], uri
    )
    assert isinstance(r, RegistryResponse)
    assert len(r.applications) == 2
    assert r.query_uri == uri
    assert r.has_references
    assert r.success
    assert r.count == 5

    r = _get_registry_response([app_response_success_ref, app_response_nosuccess], uri)
    assert isinstance(r, RegistryResponse)
    assert len(r.applications) == 2
    assert r.query_uri == uri
    assert r.has_references
    assert not r.success
    assert r.count == 2

    r = _get_registry_response(
        [app_response_success_noref, app_response_success_noref2], uri
    )
    assert isinstance(r, RegistryResponse)
    assert len(r.applications) == 2
    assert r.query_uri == uri
    assert not r.has_references
    assert r.success
    assert r.count == 0

    r = _get_registry_response(
        [app_response_success_noref, app_response_success_noref2], uri
    )
    assert isinstance(r, RegistryResponse)
    assert len(r.applications) == 2
    assert r.query_uri == uri
    assert not r.has_references
    assert r.success
    assert r.count == 0

    r = _get_registry_response([app_response_nosuccess, app_response_nosuccess2], uri)
    assert isinstance(r, RegistryResponse)
    assert len(r.applications) == 2
    assert r.query_uri == uri
    assert not r.has_references
    assert not r.success
    assert r.count == 0
