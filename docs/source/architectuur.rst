============
Architectuur
============

Dit is een uitwerking van optie 1 (zie opmerkingen)

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

    node "RestRegistry" as RR{
      [Registry] as REG
      [Aggregator] as AGR
    }

    package "App 1" as A1{
        [ReferencesPlugin] as RP1
    }

    package "App 2" as A2{
        [ReferencesPlugin] as RP2
    }

    RP -> REG
    REG -> RP1
    REG -> RP2
    RP1 -> AGR
    RP2 -> AGR
    AGR -> RP

    @enduml


Plugin
------

De plugin zal een route configuren op "/references", de implementatie van de view wordt overgelaten aan de desbetreffende applicatie.
De registry kan dan "/references?uri=http://id.erfgoed.net/foobar/1" gebruiken om aan de applicatie te vragen of er nog een referentie is naar een bepaalde resource

Er wordt ook voorzien in een "isReferenced(uri)" methode. Deze zal de centrale registry aanroepen en teruggeven of een uri nog referenties heeft.


Registry
--------

Centrale registry

.. uml::

    @startuml

    object "application" as APP

    APP: id
    APP: name


    object "reference" as REF

    REF: app_id
    REF: uri_id


    object "uri" as URI

    URI: uri_id
    URI: base_uri


    APP - REF
    REF - URI

    @enduml

