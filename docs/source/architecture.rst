============
Architecture
============

Schema
------

.. uml::

    @startuml

    package "Client" as AB{
        interface " " as START
        [pyramid_urireferencer] as RP
        START -> RP
    }

    node "UriRegistry" as UR{
      [Registry] as REG
    }

    package "Application 1" as A1{
        [pyramid_urireferencer] as RP1
    }

    package "Application 2" as A2{
        [pyramid_urireferencer] as RP2
    }

    RP -> REG
    REG -> RP1
    REG -> RP2
    RP1 -> REG
    RP2 -> REG
    REG -> RP

    @enduml

A client queries the registry with a certain URI, eg.
`http://id.erfgoed.net/foo/bar`. The registry checks if it knows any
applications that might be using this URI. It discovers that two applications
could possibly be using it. Both applications are queried. In each application a
:class:`pyramid_urireferencer.referencer.AbstractReferencer` has been configured
that can check if an incomming URI is in use in the application. The results are
sent back to the registry. The registry tallies the results and aggregates them.
A final response is sent back to the client.


pyramid_urireferencer
---------------------

This pluging will expose a service at `/references`. This service endpoint will take a
single parameter, `uri`. A full request looks like eg.
`/references?uri=http://id.erfgoed.net/besluiten/1`. Within the application, a
check will be executed to see if the application keeps references to this
particular URI.

The plugin also provides a method
:meth:`pyramid_urireferencer.referencer.Referencer.is_referenced` that can be
used to contact the central registry to see if a certain URI is in use
somewhere. This method requires a function :meth:`pyramid_urireferencer.referencer.Referencer.get_uri`
to determine the uri of the current request.
