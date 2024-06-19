import logging
import os

import yaml
from pyramid.config import Configurator

from .models import Application  # NoQa
from .models import UriTemplate  # NoQa
from .registry import _build_uri_registry  # NoQa
from .registry import get_uri_registry  # NoQa

log = logging.getLogger(__name__)


def _parse_settings(settings):
    """
    Parse the relevant settings for this application.

    :param dict settings:
    """

    log.debug(settings)

    prefix = "uriregistry"

    defaults = {
        "config": os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "sample.yaml")
        )
    }

    urireg_settings = defaults.copy()

    for short_key_name in ("config",):
        key_name = f"{prefix}.{short_key_name}"
        if key_name in settings:
            urireg_settings[short_key_name] = settings.get(
                key_name, defaults.get(short_key_name, None)
            )

    for short_key in urireg_settings:
        long_key = f"{prefix}.{short_key}"
        settings[long_key] = urireg_settings[short_key]

    return urireg_settings


def _load_configuration(path):
    """
    Load the configuration for the UriRegistry.

    :param str path: Path to the config file in YAML format.
    :returns: A :class:`dict` with the config options.
    """
    log.debug("Loading uriregistry config from %s." % path)
    f = open(path)
    content = yaml.full_load(f.read())
    log.debug(content)
    f.close()
    return content


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.

    :param pyramid.config.Configurator global_config:
    """

    config = Configurator(settings=settings)

    urireg_settings = _parse_settings(config.registry.settings)

    registryconfig = _load_configuration(urireg_settings["config"])

    _build_uri_registry(config.registry, registryconfig)

    config.add_directive("get_uri_registry", get_uri_registry)
    config.add_request_method(get_uri_registry, "uri_registry", reify=True)

    from pyramid_urireferencer.renderers import json_renderer

    config.add_renderer("json", json_renderer)

    config.add_static_view("static", "static", cache_max_age=3600)
    config.add_route("home", "/")
    config.add_route("references", "/references")

    config.scan()
    return config.make_wsgi_app()
