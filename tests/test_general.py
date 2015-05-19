import pytest

import os

from uriregistry import _load_configuration

class TestGeneral:

    def test_load_configuration(self):
        cfg = _load_configuration(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.cfg'))
        assert 'uris' in cfg
        assert 'applications' in cfg
