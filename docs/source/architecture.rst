============
Architecture
============

Een centrale registry zal bijhouden welke applicaties refereren naar een bepaalde resource (via uri). Indien de authentieke
bron van de resource wil achterhalen of er nog verwijzingen zijn naar de resource, dan de bron deze vraag stellen aan de registry.
De registry kan dan op basis van de registry informatie deze vraag doorsturen naar de benodigde applicaties. De antwoorden van de applicaties worden dan
geaggregeerd in een antwoord naar de authentieke bron.

Elke applicatie die wil kunnen refereren naar andere data dient dit te registreren in de centrale registry en moet ook een methode implementeren om
eventuele referenties op te vragen.

Er zal een plugin voorzien worden die een genrieke methode voorziet om de registry aan te spreken.
Deze plugin zal ook een interface bevatten voor de methode om referenties op te vragen van de desbetreffende applicatie.


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
