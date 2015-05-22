============
Architecture
============

Schema
------

.. uml::

    @startuml

    package "Authentieke bron" as AB{
        interface " " as START
        [ReferencesPlugin] as RP
        START -> RP
    }

    node "UriRegistry" as UR{
      [Registry] as REG
      [Aggregator] as AGR
    }

    package "App 1" as A1{
        [pyramid_urireferencer] as RP1
    }

    package "App 2" as A2{
        [pyramid_urireferencer] as RP2
    }

    RP -> REG
    REG -> RP1
    REG -> RP2
    RP1 -> AGR
    RP2 -> AGR
    AGR -> RP

    @enduml


pyramid_urireferencer
---------------------

This pluging will expose a service at `/references`. This service will take a
single parameter, `uri`. A full request looks like eg.
`/references?uri=http://id.erfgoed.net/besluiten/1`. Within the application, a
check will be executed to see if the application keeps references to this
particular URI.

The plugin also provides a method
:meth:`pyramid_urireferencer.referencer.Referencer.is_referenced` that can be
used to contact the central registry to see if a certain URI is in use
somewhere.
