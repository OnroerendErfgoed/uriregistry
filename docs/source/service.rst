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
        * **service_url** - Url of the application's references service
        * **uri** - Uri of the  application. Does not need to be a http uri.
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
            "success": true,
            "has_references": true,
            "count": 8,
            "applications": [
                {
                    "count": 8,
                    "title": "app1",
                    "success": true,
                    "has_references": true,
                    "uri": "http://www.erfgoed.net",
                    "service_url": "http://www.erfgoed.net/references",
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
                   "service_url": "http://something.erfgoed.net/references",
                   "uri": "http://something.erfgoed.net",
                   "items": null
                }
            ],
        }

    :query uri: The uri of the resource the client wants information on. Required.
    :statuscode 200: The service has a valid answer
    :statuscode 400: There's something wrong with the request, eg. no URI parameter present.


---------------------
Pyramid_urireferencer
---------------------

Every application that implements :mod:`pyramid_urireferencer` has the samen
endpoint as the central registry, but with a slightly different response set.

.. http:get:: /references

    Query the application to see if and possibly where a certain URI is in use. 

    **Example request**:

    .. sourcecode:: http

        GET /references?uri=http://id.erfgoed.net/foobar/2
        Host: www.erfgoed.net
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "count": 8,
            "title": "app1",
            "success": true,
            "has_references": true,
            "uri": "http://www.erfgoed.net",
            "service_url": "http://www.erfgoed.net/references",
            "items": [
                {
                   "name": "itemname1",
                   "uri": "http://www.erfgoed.net/baz/1"
                }, {
                   "name": "itemname2",
                   "uri": "http://www.erfgoed.net/baz/10"
                }, {
                   "name": "itemname3",
                   "uri": "http://www.erfgoed.net/baz/14"
                }, {
                   "name": "itemname4",
                   "uri": "http://www.erfgoed.net/baz/34"
                }
            ]
        }

    :query uri: The uri of the resource the client wants information on. Required.
    :statuscode 200: The service has a valid answer
    :statuscode 400: There's something wrong with the request, eg. no URI parameter present.
