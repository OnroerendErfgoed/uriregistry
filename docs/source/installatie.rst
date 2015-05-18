================
Installatie Info
================

RestRegistry heeft verschillende componenten:

    - registry: Dit is de applicatie die instaat voor het controleren van referenties bij andere applicaties
    - referencesPlugin: Dit is een pyramidplugin. Deze moet worden ingeplugd door alle applicaties die uri-referenties hebben naar authentieke bronnen
    - registrycommons: Deze library bevat de common objects voor uitwisseling van data tussen de registry en referencesPlugin.
        Bovenstaande componenten moeten een referentie hebben naar deze library


Algemene opzet
^^^^^^^^^^^^^^
Binnenhalen van de code via github

.. code::

    git clone https://github.com/OnroerendErfgoed/restregistry.git


Aanmaken van een virtualenvironment

.. code::

    mkvirtualenv restregistry
    (workon restregistry)

Installeren van requirements

.. code::

    pip install -r requirements(-dev).txt

Installeren van registrycommons in de virtuele omgeving.

.. code::

    /registrycommons
        workon restregistry
        python setup.py develop
        pip install -r requirements-dev.txt

Opzetten registry
^^^^^^^^^^^^^^^^^
Installeren van registry in de virtuele omgeving.

.. code::

    /registry
        workon restregistry
        python setup.py develop
        pip install -r requirements-dev.txt
        pserve development.ini

De registry-applicatie is nu opgestart op http://localhost:6543 en heeft '/references?uri=' beschikbaar als endpoint.

De configuratie van welke uri's en welke applicaties (+ onderlinge relaties) zijn opgenomen in de registry konoan worden ingesteld in 'registry.cfg' (json).

.. code::

    {"uri":  [
                {
                "id": "1",
                "base_uri": "http://id.erfgoed.net/foobar",
                "applications": ["1", "2"]
                },
                {
                "id": "2",
                "base_uri": "http://id.erfgoed.net/bar/",
                "applications": ["1"]
                },
                {
                "id": "3",
                "base_uri": "http://id.erfgoed.net/foo/",
                "applications": ["2"]
                }
           ],
    "application":  [
                {
                "id": "1",
                "name": "app1",
                "url": "http://localhost:5555",
                "uri": "http://localhost:5555"
                },
                {
                "id": "2",
                "name": "app2",
                "url": "http://localhost:2222",
                "uri": "http://localhost:2222"
                }
                ]
    }

Opzetten referencesPlugin
^^^^^^^^^^^^^^^^^^^^^^^^^
Installeren van referencesPlugin in de virtuele omgeving.

.. code::

    /referencesplugin
        workon restregistry
        python setup.py develop
        pip install -r requirements-dev.txt

referencesplugin is zelf geen applicatie, maar kan worden ingeplugd in een andere applicatie.
Inpluggen van de referencesplugin kan op basis van volgende stappen:

- Toevoegen van de plugin in de __init__.py main-method van de applicatie

    .. code::

        def main(global_config, **settings):
            """ This function returns a Pyramid WSGI application.
            """
            config = Configurator(settings=settings)
            config.include('pyramid_chameleon')
            config.add_static_view('static', 'static', cache_max_age=3600)
            config.add_route('home', '/')
            config.include('referencesplugin')
            config.scan()
            return config.make_wsgi_app()

- Toevoegen van referenties in (development).ini file

    .. code::

        #settings for the restregistry
        restregistry.referencer = app_demo.DemoReferencer
        restregistry.registry_url = http://localhost:6543

    *restregistry.referencer: Dit is een tekstuele verwijzing naar de implementerende class van de abastracte Referencer class

    *restregistry.registry_url = url waar de registry-applicatie zich situeert

- Implementeren van de referencer-method van de Referencer-class
    **Example implementation**:
        .. code::

            class DemoReferencer(Referencer):
                def references(self, uri):
                    try:
                        #search for reference in the demo app based on internal application logics
                        has_references = True
                        count = 8
                        items = []
                        for x in range(1, 5):
                            items.append(Item("itemname_" + str(x), "http://demo_uri/" + str(x)))
                        success = True
                    except:
                        has_references = None
                        count = None
                        items = None
                        success = False
                    return ApplicationResponse(None, None, None, success, has_references, count, items)