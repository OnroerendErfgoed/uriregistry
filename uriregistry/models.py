# -*- coding: utf-8 -*-

import re

class Uri:
    def __init__(self, id, match_uri, applications):
        self.id = id
        self.match_uri = re.compile(match_uri)
        self.applications = applications

    def matches(self, uri):
        res = self.match_uri.match(uri)
        return res is not None

class Application:
    def __init__(self, id, name, uri, url):
        self.id = id
        self.uri = uri
        self.url = url
        self.name = name
