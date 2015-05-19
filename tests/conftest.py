import pytest

from uriregistry.registry import UriRegistry

@pytest.fixture(scope="session")
def registryconfig():
    cfg = {
        'uris': [
            {
                'id': '1',
                'match_uri': 'http://id.erfgoed.net/foobar/\d+',
                'applications': ['1', '2']
            }, {
                'id': '2',
                'match_uri': 'http://id.erfgoed.net/bar/\w+',
                'applications': ['1']
            }, {
                'id': '3',
                'match_uri': 'http://id.erfgoed.net/foo/.+',
                'applications': ['2']
            }
        ],
        'applications': [
            {
                'id': '1',
                'name': 'app1',
                'url': 'http://localhost:5555',
                'uri': 'http://localhost:5555'
            }, {
                'id': '2',
                'name': 'app2',
                'url': 'http://localhost:2222',
                'uri': 'http://localhost:2222'
            }
        ]
    }
    return cfg


@pytest.fixture(scope="session")
def uriregistry(registryconfig):
    return UriRegistry(registryconfig['applications'], registryconfig['uris'])
