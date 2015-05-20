import pytest

import os

from uriregistry import (
    _parse_settings,
    _load_configuration
)

class TestGeneral:

    def test_parse_settings(self):
        settings = {
            'uriregistry.config': os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.yaml')
        }
        args = _parse_settings(settings)
        assert 'config' in args
        assert args['config'] == os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.yaml')

    def test_load_configuration(self):
        cfg = _load_configuration(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.yaml'))
        assert 'uris' in cfg
        assert 'applications' in cfg
