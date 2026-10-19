============
Architecture
============

Schema
------

.. uml::

    @startuml

    package "Client" as AB{
        interface " " as START
        [urireferencer] as RP
        START -> RP
    }

    node "UriRegistry" as UR{
      [Registry] as REG
    }

    package "Application 1" as A1{
        [urireferencer] as RP1
    }

    package "Application 2" as A2{
        [urireferencer] as RP2
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
could possibly be using it. Both applications are queried through their
references service, which checks if the incoming URI is in use in that
application. The results are sent back to the registry. The registry tallies the
results and aggregates them. A final response is sent back to the client.


The application side
--------------------

Each application has two responsibilities, both described in :doc:`service`:

* Expose a references service at `/references`. This service endpoint takes a
  single parameter, `uri`. A full request looks like eg.
  `/references?uri=http://id.erfgoed.net/besluiten/1`. Within the application, a
  check is executed to see if the application keeps references to this
  particular URI.
* Before an operation that would break references, such as deleting a resource,
  ask the central registry whether the resource's URI is still in use, and
  refuse the operation if it is.

How an application implements this is up to the application, as long as it
follows the contract. For Pyramid applications, :mod:`pyramid_urireferencer`
provides both: it exposes the `/references` service and offers
:meth:`pyramid_urireferencer.referencer.Referencer.is_referenced` to contact the
central registry. See :doc:`development`.
