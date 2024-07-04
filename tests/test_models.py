from uriregistry.models import UriTemplate


class TestUri:

    def test_numeric_matches(self):
        u = UriTemplate(r"http://id.erfgoed.net/foobar/\d+$", [])
        assert u.matches("http://id.erfgoed.net/foobar/1")
        assert u.matches("http://id.erfgoed.net/foobar/12")
        assert u.matches("http://id.erfgoed.net/foobar/123456789")
        assert not u.matches("http://id.erfgoed.net/foo/a")
        assert not u.matches("http://id.erfgoed.net/bar/a")
        assert not u.matches("http://id.erfgoed.net/foobar/a")
        assert not u.matches("http://id.erfgoed.net/foobar")
        assert not u.matches("http://id.erfgoed.net/foobar/1a")

    def test_alphanumeric_matches(self):
        u = UriTemplate(r"http://id.erfgoed.net/foobar/\w+$", [])
        assert u.matches("http://id.erfgoed.net/foobar/a")
        assert u.matches("http://id.erfgoed.net/foobar/at")
        assert u.matches("http://id.erfgoed.net/foobar/baz")
        assert u.matches("http://id.erfgoed.net/foobar/1")
        assert not u.matches("http://id.erfgoed.net/foobar")
        assert not u.matches("http://id.erfgoed.net/foobar/1-a")
