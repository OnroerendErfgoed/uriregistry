# -*- coding: utf-8 -*-

from zope.interface import Interface

from .models import Application, Uri

class IUriRegistry(Interface):
    pass

class UriRegistry:

    def __init__(self, applications = [], uris = []):
        self.applications = [Application(app['id'], app['name'], app['uri'], app['url']) for app in applications]
        self.uris = [
            Uri(
                u['id'],
                u['base_uri'],
                [app for app in self.applications if app.id in u['applications']]
            ) for u in uris
        ]

def _build_uri_registry(registry, registryconfig):
    uri_registry = registry.queryUtility(IUriRegistry)
    if uri_registry is not None:
        return uri_registry

    uri_registry = UriRegistry(
        registryconfig['applications'],
        registryconfig['uris']
    )

    registry.registerUtility(uri_registry, IUriRegistry)
    return registry.queryUtility(IUriRegistry)

def get_uri_registry(registry):
    '''
    Get the :class:`uriregistry.registry.UriRegistry` attached to this pyramid
    application.

    :rtype: :class:`uriregistry.registry.Registry`
    '''
    #Argument might be a config or request
    regis = getattr(registry, 'registry', None)
    if regis is None:
        regis = registry
    return regis.queryUtility(IUriRegistry)
