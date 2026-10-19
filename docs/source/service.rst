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
                           "title": "itemname1",
                           "uri": "http://www.erfgoed.net/baz/1"
                        }, {
                           "title": "itemname_2",
                           "uri": "http://www.erfgoed.net/baz/10"
                        }, {
                           "title": "itemname_3",
                           "uri": "http://www.erfgoed.net/baz/14"
                        }, {
                           "title": "itemname_4",
                           "uri": "http://www.erfgoed.net/baz/34"
                        }
                    ]
                }, {
                   "count": null,
                   "title": "app2",
                   "success": false,
                   "has_references": null,
                   "service_url": "http://something.erfgoed.net/references",
                   "uri": "http://something.erfgoed.net",
                   "items": null
                }
            ]
        }

    :query uri: The uri of the resource the client wants information on. Required.
    :statuscode 200: The service has a valid answer
    :statuscode 400: There's something wrong with the request, eg. no URI parameter present.


-------------------------------
Application references service
-------------------------------

Every application in the network exposes the same endpoint as the central
registry, but answers only for itself. This is a contract, not a library: any
application that implements it can be registered with the UriRegistry, whatever
framework it is built with. :mod:`pyramid_urireferencer` implements it for
Pyramid applications.

The endpoint has to be served at the ``service_url`` configured for the
application in the registry, typically ``<application>/references``. The
registry does not send an ``Accept`` header, so the application must answer
with JSON regardless.

.. http:get:: /references

    Query the application to see if and possibly where a certain URI is in use.

    **Structure of a response**:

    * **title** - A title for the application
    * **uri** - Uri of the application. Does not need to be a http uri.
    * **service_url** - Url of this references service
    * **success** - `True` if the application could check its references, else `False`.
    * **has_references** - `True` if at least one reference was found. `None` (not `False`) if the check failed.
    * **count** - The number of references found. `None` if the check failed.
    * **items** - A list of resources that reference the URI in question, at most 5. `None` if the check failed.

        * **title** - Title of the resource
        * **uri** - Uri of the resource

    Every field is always present; when the check fails, the application still
    answers ``200`` with ``success`` set to `False` and ``has_references``,
    ``count`` and ``items`` set to `None`.

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
                   "title": "itemname1",
                   "uri": "http://www.erfgoed.net/baz/1"
                }, {
                   "title": "itemname2",
                   "uri": "http://www.erfgoed.net/baz/10"
                }, {
                   "title": "itemname3",
                   "uri": "http://www.erfgoed.net/baz/14"
                }, {
                   "title": "itemname4",
                   "uri": "http://www.erfgoed.net/baz/34"
                }
            ]
        }

    :query uri: The uri of the resource the client wants information on. Required.
    :statuscode 200: The service has a valid answer
    :statuscode 400: There's something wrong with the request, eg. no URI parameter present.

    **Example response when the check failed**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "count": null,
            "title": "app1",
            "success": false,
            "has_references": null,
            "uri": "http://www.erfgoed.net",
            "service_url": "http://www.erfgoed.net/references",
            "items": null
        }


--------------------
Protected operations
--------------------

Before an application performs an operation that would break references, such
as deleting a resource, it asks the central registry whether the resource's URI
is still in use. If it is, or if the registry could not confirm that it is not,
the operation is refused with the following response:

* **409 Conflict** - At least one application still references the URI.
* **500 Internal Server Error** - The registry, or one of the applications it
  queried, could not be checked. The operation is refused rather than risking
  broken references.

**Structure of a response**:

* **message** - A human readable summary.
* **errors** - One message per application that still references the URI (409)
  or could not be checked (500).
* **registry_response** - The full response of the central registry, see
  :http:get:`/references`.

**Example response**:

.. sourcecode:: http

    HTTP/1.1 409 Conflict
    Content-Type: application/json

    {
        "message": "The uri http://id.erfgoed.net/foobar/2 is still in use by other applications. A total of 1 references have been found.",
        "errors": [
            "http://www.erfgoed.net: 1 references found, such as http://www.erfgoed.net/baz/1"
        ],
        "registry_response": {
            "query_uri": "http://id.erfgoed.net/foobar/2",
            "success": true,
            "has_references": true,
            "count": 1,
            "applications": [
                {
                    "title": "app1",
                    "uri": "http://www.erfgoed.net",
                    "service_url": "http://www.erfgoed.net/references",
                    "success": true,
                    "has_references": true,
                    "count": 1,
                    "items": [
                        {
                            "title": "itemname1",
                            "uri": "http://www.erfgoed.net/baz/1"
                        }
                    ]
                }
            ]
        }
    }
