# -*- coding: utf-8 -*-

import re

class Uri:
    '''
    Represents the config for a certain uri.
    '''
    def __init__(self, id, match_uri, applications):
        self.id = id
        self.match_uri = re.compile(match_uri)
        self.applications = applications

    def matches(self, uri):
        res = self.match_uri.match(uri)
        return res is not None

class Application:
    '''
    Represents the config for an application.
    '''
    def __init__(self, id, title, uri, url):
        self.id = id
        self.uri = uri
        self.url = url
        self.title = title
