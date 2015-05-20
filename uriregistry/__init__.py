# -*- coding: utf-8 -*-

import logging
log = logging.getLogger(__name__)

from pyramid.config import Configurator

import os
import json

from .models import Application, Uri
from .registry import get_uri_registry, _build_uri_registry


def _parse_settings(settings):

    log.debug(settings)

    prefix='uriregistry'

    defaults = {
        'config': os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sample.cfg'))
    }

    urireg_settings = defaults.copy()

    for short_key_name in ('config', ):
        key_name = '%s.%s' % (prefix, short_key_name)
        if key_name in settings:
            urireg_settings[short_key_name] = \
                settings.get(key_name, defaults.get(short_key_name, None))

    for short_key in urireg_settings:
        long_key = '%s.%s' % (prefix, short_key)
        settings[long_key] = urireg_settings[short_key]

    return urireg_settings

def _load_configuration(path):
    log.debug('Loading uriregistry config from %s.' % path)
    f = open(path, 'r')
    content = json.loads(f.read())
    f.close()
    return content

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    config = Configurator(settings=settings)

    urireg_settings = _parse_settings(config.registry.settings)

    registryconfig = _load_configuration(urireg_settings['config'])

    _build_uri_registry(config.registry, registryconfig)

    config.add_directive('get_uri_registry', get_uri_registry)
    config.add_request_method(get_uri_registry, 'uri_registry', reify=True)

    from pyramid_urireferencer.renderers import json_renderer
    config.add_renderer('json', json_renderer)

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('references', '/references')

    config.scan()
    return config.make_wsgi_app()
