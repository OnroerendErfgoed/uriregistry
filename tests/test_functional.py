import os

import pytest
from webtest import TestApp


@pytest.fixture()
def app():
    settings = {
        "uriregistry.config": os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "test.yaml"
        )
    }
    from uriregistry import main

    return TestApp(main({}, **settings))


class TestFunctional:

    def test_home(self, app):
        res = app.get("/")
        assert res.status == "200 OK"

    def test_get_features_without_uri(self, app):
        res = app.get("/references", status=400)
        assert res.status == "400 Bad Request"

    def test_get_features_with_uri(self, app):
        res = app.get("/references?uri=http://id.erfgoed.net/foo/1")
        assert res.status == "200 OK"
        assert "application/json" in res.headers["Content-Type"]

    def test_get_features_with_or_regex(self, app):
        res = app.get("/references?uri=http://id.erfgoed.net/bal/789")
        assert res.status == "200 OK"
        data_bal = res.json
        assert len(data_bal["applications"]) == 1
        res = app.get("/references?uri=http://id.erfgoed.net/bak/232")
        assert res.status == "200 OK"
        data_bak = res.json
        assert len(data_bak["applications"]) == 1
        assert data_bal["applications"] == data_bak["applications"]
