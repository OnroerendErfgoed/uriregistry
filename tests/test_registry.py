import os
import unittest

from pyramid import testing
from pyramid.response import Response

from uriregistry import _load_configuration
from uriregistry.registry import UriRegistry
from uriregistry.models import Application
from uriregistry.views import _get_base_uri, _handle_uri, _eq, _stripped, _get_application_response, _get_registry_response, \
    RegistryView
from pyramid_urireferencer.models import RegistryResponse, ApplicationResponse


class TestData(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        uri_dict = \
                [
                {
                'id': '1',
                'base_uri': 'http://id.erfgoed.net/foobar',
                'applications': ['1', '2']
                },
                {
                'id': '2',
                'base_uri': 'http://id.erfgoed.net/bar/',
                'applications': ['1']
                },
                {
                'id': '3',
                'base_uri': 'http://id.erfgoed.net/foo/',
                'applications': ['2']
                }
                ]

        application_dict =  \
                [
                {
                'id': '1',
                'name': 'app1',
                'url': 'http://localhost:5555',
                'uri': 'http://localhost:5555'
                },
                {
                'id': '2',
                'name': 'app2',
                'url': 'http://localhost:2222',
                'uri': 'http://localhost:2222'
                }
                ]
        self.uri_registry = UriRegistry(application_dict, uri_dict)

    def tearDown(self):
        pass

    def test_home(self):
        self.assertIsInstance(RegistryView(testing.DummyRequest()).home(), Response)

    def test_get_base_uri(self):
        self.assertEqual(_get_base_uri("http://id.erfgoed.net/foobar/2/"), "http://id.erfgoed.net/foobar")
        self.assertEqual(_get_base_uri("http://id.erfgoed.net/foobar/2/"), "http://id.erfgoed.net/foobar")
        self.assertEqual(_get_base_uri("http://id.erfgoed.net/foobar/2\\"), "http://id.erfgoed.net/foobar")
        self.assertEqual(_get_base_uri("http:\\\\id.erfgoed.net\\foobar\\2"), "http://id.erfgoed.net/foobar")

        self.assertNotEqual(_get_base_uri("http://id.erfgoed.net/foobar/2/"), "http://id.erfgoed.net/foobar/2")
        self.assertNotEqual(_get_base_uri("http://id.erfgoed.net/foobar/2/"), "http://id.erfgoed.net/foobar/2/")
        self.assertNotEqual(_get_base_uri("http://id.erfgoed.net/foobar/2/"), "http://id.erfgoed.net/foobar/")
        self.assertNotEqual(_get_base_uri("http://id.erfgoed.net/foobar/2/"), "2")

    def test_handle_uri(self):
        uri = "http://id.erfgoed.net/foobar/2/"
        response =_handle_uri(self.uri_registry, uri)
        self.assertIsInstance(response, RegistryResponse)
        self.assertEqual(response.uri, "http://id.erfgoed.net/foobar/2")
        self.assertEqual(response.base_uri, "http://id.erfgoed.net/foobar")

    def test_eq(self):
        self.assertEqual(_eq("http://id.ergoed.net/foo", "http://id.ergoed.net/foo/"), True)
        self.assertEqual(_eq("http://id.ergoed.net/foo", "http://id.ergoed.net/FOO"), False)

    def test_stripped(self):
        self.assertEqual(_stripped("http://id.ergoed.net/foo///  //\\"), "http://id.ergoed.net/foo")
        self.assertEqual(_stripped("http://id.ergoed.net/foo   "), "http://id.ergoed.net/foo")

    def test_get_application_response(self):
        uri = "http://id.erfgoed.net/foobar/2/"
        app = Application(1, "app_name", "http://uri/app", "http://url/app")
        r = _get_application_response(app, uri)
        self.assertIsInstance(r, ApplicationResponse)
        self.assertEqual(r.uri, app.uri)
        self.assertEqual(r.url, app.url)
        self.assertEqual(r.name, app.name)
        self.assertEqual(r.success, False)

    def test_get_registry_response(self):
        uri = "http://id.erfgoed.net/foobar/2/"
        base_uri=_get_base_uri(uri)
        app_response_success_ref = ApplicationResponse("app2_name", "http://uri/app2", "http://url/app2", True, True, 2, [])
        app_response_success_ref2 = ApplicationResponse("app2_name", "http://uri/app2", "http://url/app2", True, True, 3, [])
        app_response_nosuccess = ApplicationResponse("app2_name", "http://uri/app2", "http://url/app2", False, None, None, None)
        app_response_nosuccess2 = ApplicationResponse("app2_name", "http://uri/app2", "http://url/app2", False, None, None, None)
        app_response_success_noref = ApplicationResponse("app2_name", "http://uri/app2", "http://url/app2", True, False, None, None)
        app_response_success_noref2 = ApplicationResponse("app2_name", "http://uri/app2", "http://url/app2", True, False, None, None)

        r = _get_registry_response([app_response_success_ref,app_response_success_ref2], uri, base_uri)
        self.assertIsInstance(r, RegistryResponse)
        self.assertEqual(r.applications.__len__(), 2)
        self.assertEqual(r.uri, uri)
        self.assertEqual(r.base_uri, base_uri)
        self.assertEqual(r.has_references, True)
        self.assertEqual(r.success, True)
        self.assertEqual(r.count, 5)

        r = _get_registry_response([app_response_success_ref,app_response_nosuccess], uri, base_uri)
        self.assertIsInstance(r, RegistryResponse)
        self.assertEqual(r.applications.__len__(), 2)
        self.assertEqual(r.uri, uri)
        self.assertEqual(r.base_uri, base_uri)
        self.assertEqual(r.has_references, True)
        self.assertEqual(r.success, False)
        self.assertEqual(r.count, 2)

        r = _get_registry_response([app_response_success_noref, app_response_success_noref2], uri, base_uri)
        self.assertIsInstance(r, RegistryResponse)
        self.assertEqual(r.applications.__len__(), 2)
        self.assertEqual(r.uri, uri)
        self.assertEqual(r.base_uri, base_uri)
        self.assertEqual(r.has_references, False)
        self.assertEqual(r.success, True)
        self.assertEqual(r.count, 0)

        r = _get_registry_response([app_response_success_noref, app_response_success_noref2], uri, base_uri)
        self.assertIsInstance(r, RegistryResponse)
        self.assertEqual(r.applications.__len__(), 2)
        self.assertEqual(r.uri, uri)
        self.assertEqual(r.base_uri, base_uri)
        self.assertEqual(r.has_references, False)
        self.assertEqual(r.success, True)
        self.assertEqual(r.count, 0)

        r = _get_registry_response([app_response_nosuccess, app_response_nosuccess2], uri, base_uri)
        self.assertIsInstance(r, RegistryResponse)
        self.assertEqual(r.applications.__len__(), 2)
        self.assertEqual(r.uri, uri)
        self.assertEqual(r.base_uri, base_uri)
        self.assertEqual(r.has_references, False)
        self.assertEqual(r.success, False)
        self.assertEqual(r.count, 0)
