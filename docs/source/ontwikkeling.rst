.. _ontwikkeling:

============
Ontwikkeling
============

Benodigdheden
=============

- Python(versie 2.7, 3.3 of 3.4)
- registrycommons

Beginnen met ontwikkeling
=========================

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

Testing
=======
pytest wordt gebruikt voor het testen van de code:

*unit tests: testen voor een afgezonderd gedeelte van de code: een class, een method,...
*integration tests: testen van de integratie en interactie over verschillende packages

tox wordt gebruikt voor het samenstellen van een test'scenario'
Via tox.ini wordt geconfigureerd welke tests moeten worden uitgevoerd en tegen welke python omgevingen getest moet worden.
restregistry wordt getest tov python 2.7, 3.3 en 3.4

.. code-block:: bash

    # Run unit & integration tests for all environments
    $ tox
    # No coverage
    $ py.test
    # Coverage
    $ py.test --cov restregistry --cov-report term-missing

Unit tests
^^^^^^^^^^

.. code-block:: bash

    # Only run unit tests for a specific package
    $ py.test registry/tests
    $ py.test referencesplugin/tests
    $ py.test registrycommons/tests


Integration tests
^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # Only run integration tests
    $ py.test restregistry/tests/test_integration.py