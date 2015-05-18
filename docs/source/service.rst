====================
Service Documentatie
====================
--------
Registry
--------

De volgende endpoints zijn gekend:

.. http:get:: /references?uri=

    Het opvragen aan de registry van referenties naar een opgegeven uri

    **Request**:

        * **uri** - unieke verwijzing naar een object (uri). De service gaat op zoek naar referenties in andere applicaties naar dit object

    **Response**:

        * **request** - de gebruikte request parameters
            * **uri** - uri waarvoor referenties gezocht worden
        * **response** - de response-informatie van de registry
            * **base_uri** - de base uri, afgeleid van de uri
            * **success** - is 'true' als alle requests gelukt zijn vanuit de registry naar de refererende applicaties, zoniet 'false'
            * **has_references** - is 'true' als er een applicatie is die referenties heeft naar de uri, anders 'false'
            * **count** - som van alle succesvolle gevonden referenties
            * **applications** - array van de applicaties waarin referenties gezocht zijn naar de request-uri
                * **name** - naam van de applicatie
                * **url** - url van de applicatie
                * **uri** - uri van de applicatie
                * **success** - 'true' indien de request naar de applicatie gelukt is, zoniet 'false'
                * **has_references** - 'true' indien referenties gevonden, 'false' indien geen referenties gevonden, 'null' indien success=false
                * **count** - geeft het aantal gevonden referenties, '0' indien geen referenties gevonden, 'null' indien success=false
                * **items** - geeft de objecten die verwijzen naar de uri (max. 5 objecten), 'null' indien success=false
                    * **name** - naam van het object
                    * **uri** - uri van het object dat verwijst naar de request-uri

    **Example request**:

    .. sourcecode:: http

        Remote Address:127.0.0.1:6543
        Request URL:http://localhost:6543/references?uri=http://id.erfgoed.net/foobar/2
        Request Method:GET
        Status Code:200 OK

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
           "request":
           {
               "uri": "http://id.erfgoed.net/foobar/2"
           },
           "response":
           {
               "base_uri": "http://id.erfgoed.net/foobar",
               "count": 8,
               "applications":
               [
                   {
                       "count": 8,
                       "name": "app1",
                       "success": true,
                       "has_references": true,
                       "url": "http://localhost:5555",
                       "items":
                       [
                           {
                               "name": "itemname_1",
                               "uri": "http://demo_uri/1"
                           },
                           {
                               "name": "itemname_2",
                               "uri": "http://demo_uri/2"
                           },
                           {
                               "name": "itemname_3",
                               "uri": "http://demo_uri/3"
                           },
                           {
                               "name": "itemname_4",
                               "uri": "http://demo_uri/4"
                           }
                       ],
                       "uri": "http://localhost:5555"
                   },
                   {
                       "count": null,
                       "name": "app2",
                       "success": false,
                       "has_references": null,
                       "url": "http://localhost:2222",
                       "items": null,
                       "uri": "http://localhost:2222"
                   }
               ],
               "success": false,
               "has_references": true
           }
        }


    :statuscode 200: De opdracht is geslaagd.
    :statuscode 403: U heeft geen toegang tot de service.
    :statuscode 404: De service is niet beschikbaar.



----------------
ReferencesPlugin
----------------

De volgende endpoints zijn gekend:

.. http:get:: /references?uri=

    Het opvragen van referenties naar een opgegeven uri aan een applicatie die de ReferencesPlugin inplugt

    **Request**:

        * **uri** - unieke verwijzing naar een object (uri). De service gaat op zoek naar referenties in de applicaties die referencesplugin inplugt

    **Response**:

        * **name** - naam van de applicatie (wordt aangeleverd door registry, niet door de applicatie zelf)
        * **url** - url van de applicatie (wordt aangeleverd door registry, niet door de applicatie zelf)
        * **uri** - uri van de applicatie (wordt aangeleverd door registry, niet door de applicatie zelf)
        * **success** - 'true' indien de request naar de applicatie gelukt is, zoniet 'false'
        * **has_references** - 'true' indien referenties gevonden, 'false' indien geen referenties gevonden, 'null' indien success=false
        * **count** - geeft het aantal gevonden referenties, '0' indien geen referenties gevonden, 'null' indien success=false
        * **items** - geeft de objecten die verwijzen naar de uri (max. 5 objecten), 'null' indien success=false
            * **name** - naam van het object
            * **uri** - uri van het object dat verwijst naar de request-uri

    **Example request**:

    .. sourcecode:: http

        Remote Address:127.0.0.1:5555
        Request URL:http://localhost:5555/references?uri=http://id.erfgoed.net/foobar/2
        Request Method:GET
        Status Code:200 OK

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
          "count": 8,
          "name": null,
          "success": true,
          "has_references": true,
          "url": null,
          "items": [
            {
              "name": "itemname_1",
              "uri": "http://demo_uri/1"
            },
            {
              "name": "itemname_2",
              "uri": "http://demo_uri/2"
            },
            {
              "name": "itemname_3",
              "uri": "http://demo_uri/3"
            },
            {
              "name": "itemname_4",
              "uri": "http://demo_uri/4"
            }
          ],
          "uri": null
        }

    :statuscode 200: De opdracht is geslaagd.
    :statuscode 403: U heeft geen toegang tot de service.
    :statuscode 404: De service is niet beschikbaar.


