========
Services
========

-----------
UriRegistry
-----------

The central UriRegistry has a single endpoint that can be called.

.. http:get:: /references

    Query the registry to see if and possibly where a URI is in use.

    **Structure of a response**:

    * **query_uri** - the URI we're looking for
    * **success** - Did the registry succeed in querying the underlying
        services. Will be `True` if all requests succeeded, else `False`.
    * **has_references** - Will be `True` as soon as one application has at
        least one reference to the item in question.
    * **count** - How many references were found in total?
    * **applications** - A list of all applications that were queries and the results they returned

        * **title** - A title for the application
        * **url** - url of the application
        * **uri** - uri of the  applicatie
        * **success** - Will be `True` if the request for this application succeeded, else `False`.
        * **has_references** - Will be `True` if at least one reference was found. If the request failed, this will be `None`. Not `False`.
        * **count** - Returns the number of references found. If the request failed (success==`False`), this will be `None`.
        * **items** - A list of resoures that have a reference to the URI in question. For performance reasons, a maximum of 5 resources is allowed. If the request failed, this will be `None`.

            * **title** - Title of the resource
            * **uri** - Uri of the resource

    **Example request**:

    .. sourcecode:: http

        GET /references?uri=http://id.erfgoed.net/foobar/2
        Host: uriregistry.org
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "query_uri": "http://id.erfgoed.net/foobar/2",
            "success": false,
            "has_references": true,
            "count": 8,
            "applications": [
                {
                    "count": 8,
                    "title": "app1",
                    "success": true,
                    "has_references": true,
                    "uri": "http://www.erfgoed.net",
                    "url": "http://www.erfgoed.net",
                    "items": [
                        {
                           "name": "itemname1",
                           "uri": "http://www.erfgoed.net/baz/1"
                        }, {
                           "name": "itemname_2",
                           "uri": "http://www.erfgoed.net/baz/10"
                        }, {
                           "name": "itemname_3",
                           "uri": "http://www.erfgoed.net/baz/14"
                        }, {
                           "name": "itemname_4",
                           "uri": "http://www.erfgoed.net/baz/34"
                        }
                    ],
                }, {
                   "count": null,
                   "title": "app2",
                   "success": false,
                   "has_references": null,
                   "url": "http://something.erfgoed.net",
                   "uri": "http://something.erfgoed.net",
                   "items": null
                }
            ],
        }

    :query uri: The uri of the resources the client wants information on. Required.
    :statuscode 200: The service has a valid answer
    :statuscode 400: There's something wrong with the request, eg. no URI parameter present.


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


