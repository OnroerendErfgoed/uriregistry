from uriregistry.registry import IUriRegistry
from uriregistry.registry import UriRegistry
from uriregistry.registry import _build_uri_registry
from uriregistry.registry import get_uri_registry


class TestRegistry:

    def test_get_applications_no_match(self, uriregistry):
        apps = uriregistry.get_applications("http://nudge.nudge.wink.wink")
        assert len(apps) == 0

    def test_get_applications_numeric_matches(self, uriregistry):
        apps = uriregistry.get_applications("http://id.erfgoed.net/foobar/1")
        assert len(apps) == 2

        apps = uriregistry.get_applications("http://id.erfgoed.net/foo/a")
        assert len(apps) == 1

    def test_get_applications_alphanumeric_matches(self, uriregistry):
        apps = uriregistry.get_applications("http://id.erfgoed.net/foobar/a")
        assert len(apps) == 0


class MockRegistry:

    def __init__(self, settings=None):

        if settings is None:
            self.settings = {}
        else:  # pragma NO COVER
            self.settings = settings

        self.uri_registry = None

    def queryUtility(self, iface):
        return self.uri_registry

    def registerUtility(self, uri_registry, iface):
        self.uri_registry = uri_registry


class TestGetAndBuild:

    def test_get_uri_registry(self, registryconfig):
        r = MockRegistry()
        UR = UriRegistry(
            registryconfig["applications"], registryconfig["uri_templates"]
        )
        r.registerUtility(UR, IUriRegistry)
        UR2 = get_uri_registry(r)
        assert UR == UR2

    def test_build_uri_registry_already_exists(self, registryconfig):
        r = MockRegistry()
        UR = UriRegistry(
            registryconfig["applications"], registryconfig["uri_templates"]
        )
        r.registerUtility(UR, IUriRegistry)
        UR2 = _build_uri_registry(r, registryconfig)
        assert UR == UR2

    def test_build_uri_registry(self, registryconfig):
        r = MockRegistry()
        UR = _build_uri_registry(r, registryconfig)
        assert isinstance(UR, UriRegistry)
