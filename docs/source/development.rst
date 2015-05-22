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
that extends the :class:`pyramid_urireferencer.referencer.Referencer` and
implement the :meth:`~pyramid_urireferencer.referencer.Referencer.references`
method.

.. code-block:: python
    from pyramid_urireferencer.referencer import Referencer
    from pyramid_urireferencer.models import ApplicationResponse

    class DemoReferencer(Referencer):

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
            return ApplicationResponse(None, None, None, success, has_references, count, items)

