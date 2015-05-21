# -*- coding: utf-8 -*-

from zope.interface import Interface

from .models import Application, Uri

class IUriRegistry(Interface):
    pass

class UriRegistry:
    '''
    Central registry that tracks uris and the applications they are being used in.
    '''

    def __init__(self, applications = [], uris = []):
        self.applications = [Application(app['id'], app['name'], app['uri'], app['url']) for app in applications]
        self.uris = [
            Uri(
                u['id'],
                u['match_uri'],
                [app for app in self.applications if app.id in u['applications']]
            ) for u in uris
        ]

    def get_applications(self, uri):
        '''
        Get all applications that might have a reference to this URI.

        :param string uri: Uri for which the applications need to be found.
        '''
        applications = []
        for u in self.uris:
            if u.matches(uri):
                applications.extend(u.applications)
        applications = list(set(applications))
        return applications

def _build_uri_registry(registry, registryconfig):
    '''
    :param pyramid.registry.Registry registry: Pyramid registry
    :param dict registryconfig: UriRegistry config in dict form.
    :rtype: :class:`uriregistry.registry.UriRegistry`
    '''
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

    :rtype: :class:`uriregistry.registry.UriRegistry`
    '''
    #Argument might be a config or request
    regis = getattr(registry, 'registry', None)
    if regis is None:
        regis = registry
    return regis.queryUtility(IUriRegistry)
