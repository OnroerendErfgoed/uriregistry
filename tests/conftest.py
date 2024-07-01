import pytest

from uriregistry.registry import UriRegistry


@pytest.fixture(scope="session")
def registryconfig():
    cfg = {
        "uri_templates": [
            {
                "match_uri": r"http://id.erfgoed.net/foobar/\d+",
                "applications": ["http://localhost:5555", "http://localhost:2222"],
            },
            {
                "match_uri": r"http://id.erfgoed.net/bar/\w+",
                "applications": ["http://localhost:5555"],
            },
            {
                "match_uri": r"http://id.erfgoed.net/foo/.+",
                "applications": ["http://localhost:2222"],
            },
        ],
        "applications": [
            {
                "name": "app1",
                "uri": "http://localhost:5555",
                "service_url": "http://localhost:5555/references",
            },
            {
                "name": "app2",
                "uri": "http://localhost:2222",
                "service_url": "http://localhost:2222/references",
            },
        ],
    }
    return cfg


@pytest.fixture(scope="session")
def uriregistry(registryconfig):
    return UriRegistry(registryconfig["applications"], registryconfig["uri_templates"])
