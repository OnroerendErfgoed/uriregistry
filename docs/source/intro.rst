============
Introduction
============

This project, UriRegistry, aims to solve one (and only one) problem that can
arrise when working with distributed systems. Is one of my resources being used
somewhere? This can be especially important when we want to delete a certain
resource. While in typical RESTful fashion, we cannot guarantuee a client that a
certain resource will keep on existing indefinitely, it can be a good thing to
let our end-users know that the resource is currently in use somewhere.

The basic idea is quite simple. Every application has an endpoint that can be
used by clients to ask if a certain URI is in use in that application. The
application replies if that is the case and if so with some information where
that might be the case.

Finally, there's a separate application, the UriRegistry, that can serve as a
single point of access. To ensure that a client does not need to know all the
applications that might be using one of it's resources, we use a central
registry. This central registry knows which URI is use in which application,
queries the applications in questions, gathers and tallies the results and
presents these to the client. The client itself only needs to know where the
central registry is. The registry takes care of the rest.
