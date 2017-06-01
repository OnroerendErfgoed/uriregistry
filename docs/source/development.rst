.. _development:

===========
Development
===========

Setting up a development environment
====================================

Check out the code.

.. code-block:: bash

    $ git clone https://github.com/OnroerendErfgoed/uriregistry.git


Create a virtual environment (require virtualenvwrapper).

.. code-block:: bash

    # Create a new environment
    $ mkvirtualenv uriregistry
    # Activate an existing environment
    $ workon uriregistry

Install requirements.

.. code-block:: bash

    $ pip install -r requirements-dev.txt
    $ python setup.py develop

Run the application with the sample config :file:`sample.yaml`.

.. code-block:: bash

    $ pserve development.ini

Point your browser at http://localhost:6543 to see it in action!

Configuring a UriRegistry
=========================

Your UriRegistry can be configured with a YAML file. By default, a file
:file:`sample.yaml` in the `uriregistry` package is used, but you can change
this withing your own :file:`development.ini`.

.. code-block:: ini

    uriregistry.config = %(here)s/myapp.yaml

In this config file you specify which applications can be called by the registry
when looking for URI's in use. You can also specify for each URI template in
what application it might be found.

.. code:: yaml

    applications:
        - uri: http://localhost:5555
          name: app1
          service_url: http://localhost:5555/references
        - uri: http://localhost:2222
          name: app2
          service_url: http://localhost:2222/references
    uri_templates:
        - match_uri: http://id.erfgoed.net/foobar/\d+
          applications:
            - http://localhost:5555
            - http://localhost:2222
        - match_uri: http://id.erfgoed.net/bar/\w+
          applications:
            - http://localhost:5555
        - match_uri: http://id.erfgoed.net/foo/.+
          applications:
            - http://localhost:2222

Testing
=======

Tests are run with pytest. We support the last python 2.x release and the two
most current python 3.x release. To make testing easier, use tox.

.. code-block:: bash

    # Run all tests for all environments
    $ tox
    # No coverage
    $ py.test
    # Coverage
    $ py.test --cov uriregistry --cov-report term-missing tests


Adding pyramid_urireferencer to an application
==============================================

When you want to add an application to the network of applications, you need to
include the :mod:`pyramid_urireferencer` library. Add it to your
:file:`requirements.txt` and :file:`setup.py` requirements.

Add the library to your application by including the following in your main:

.. code-block:: python

    config.include('pyramid_urireferencer')

Now you need to configure your application. Edit your :file:`development.ini`
and add two configuration options.

.. code-block:: ini

    # settings for the urireferencer
    # A dotted name indicating where your referencer can be found
    urireferencer.referencer = myapp.referencer.MyReferencer
    # The url pointing towards your own UriRegistry
    urireferencer.registry_url = http://localhost:6543

Of course, you also need to write this referencer. To do this, create an object
that implements the abstract
:class:`pyramid_urireferencer.referencer.AbstractReferencer`. Depending on your
needs it might be easier to extend the
:class:`pyramid_urireferencer.referencer.Referencer`. This class already
has a :meth:`~pyramid_urireferencer.referencer.AbstractReferencer.is_referenced`
method. But the method requires a function :meth:`get_uri` to determine the uri of the current request.
The :meth:`get_uri` still needs to be implemented. The referencer also requires you to implement the
:meth:`~pyramid_urireferencer.referencer.AbstractReferencer.references` method.

.. code-block:: python

    from pyramid_urireferencer.referencer import Referencer
    from pyramid_urireferencer.models import ApplicationResponse

    class DemoReferencer(Referencer):

        def get_uri(self, request):
            id = request.matchdict['id']
            if request.data_manager.get(aid).type == 'cirkel':
                return request.registry.settings['cirkel.uri'].format(id)
            else:
                return request.registry.settings['square.uri'].format(id)


        def references(self, uri):
            try:
                # Generate a demo response
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
            return ApplicationResponse(
                'My application',
                'http://app.me',
                'http://app.me/references',
                success,
                has_references,
                count,
                items
            )
