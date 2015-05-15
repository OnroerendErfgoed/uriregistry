import json
import os

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

def set_urilist(uri, application):
    """
    This method creates a list of :class: Uri and the :class: Application that references to this base uri
    :param uri: dictionary of base_uri with the references to applications
    :param application:  dictionary of the applications
    :return: a list of :class: Uri
    """
    global urilist
    #load dictionary and translate to Application objects
    app_list = [Application(app['id'], app['name'], app['uri'], app['url']) for app in application]
    ##load dictionary and translate to Uri objects
    urilist = [_create_uri(u, app_list) for u in uri]

def get_urilist():
    return urilist

def _create_uri(u, app_list):
    apps=[app for app in app_list if app.id in u['applications']]
    return Uri(u['id'], u['base_uri'], apps)

def _load_configuration(path):
    try:
        f = open(path, 'r')
        content = json.loads(f.read())
        f.close()
        set_urilist(content["uri"], content["application"])
    except:
        raise ImportError("configuratiefile kon niet correct gelezen worden")

_load_configuration(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'uriregistry.cfg')))





