import re


class UriTemplate:
    """
    Represents the config for a certain uri template.

    :param string match_uri: A regex that needs to be matched.
    :param list applications: A list of application uri's.
    """

    def __init__(self, match_uri, applications):
        self.id = id
        self.match_uri = re.compile(match_uri)
        self.applications = applications

    def matches(self, uri):
        """
        Does the URI match this template?

        :param string uri: URI to be matched
        :rtype: boolean
        """
        res = self.match_uri.match(uri)
        return res is not None


class Application:
    """
    Represents the config for an application.

    :param string uri: A uri that identifies the application
    :param string title: A title for the application
    :param string service_url: The url for the service that can be queried
    """

    def __init__(self, uri, title, service_url):
        self.uri = uri
        self.title = title
        self.service_url = service_url
