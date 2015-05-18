class Uri:
    def __init__(self, id, base_uri, applications):
        self.id = id
        self.base_uri = base_uri
        self.applications = applications

class Application:
    def __init__(self, id, name, uri, url):
        self.id = id
        self.uri = uri
        self.url = url
        self.name = name
