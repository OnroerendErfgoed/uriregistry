# -*- coding: utf-8 -*-

import logging
log = logging.getLogger(__name__)

from pyramid.config import Configurator

import os
import json

from .models import Application, Uri


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

def set_urilist(uri, application):
    """
    This method creates a list of :class: Uri and the :class: Application that references to this base uri
    :param uri: dictionary of base_uri with the references to applications
    :param application:  dictionary of the applications
    :return: a list of :class: Uri
    """
    global urilist
    #load dictionary and translate to Application objects
    app_list = [Application(app['id'], app['name'], app['uri'], app['url']) for app in application]
    ##load dictionary and translate to Uri objects
    urilist = [_create_uri(u, app_list) for u in uri]

def get_urilist():
    return urilist

def _create_uri(u, app_list):
    apps=[app for app in app_list if app.id in u['applications']]
    return Uri(u['id'], u['base_uri'], apps)

def _load_configuration(path):
    log.debug('Loading uriregistry config from %s.' % path)
    f = open(path, 'r')
    content = json.loads(f.read())
    f.close()
    set_urilist(content["uri"], content["application"])

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    config = Configurator(settings=settings)

    urireg_settings = _parse_settings(config.registry.settings)

    _load_configuration(urireg_settings['config'])

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('references', '/references')

    config.scan()
    return config.make_wsgi_app()
