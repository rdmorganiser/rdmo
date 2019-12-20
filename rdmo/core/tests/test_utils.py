import pytest

from ..utils import sanitize_url

urls = (
    ('', ''),
    ('/', ''),
    ('foo', 'foo'),
    ('/foo', '/foo'),
    ('/foo/', '/foo/'),
    ('foo/bar', 'foo/bar'),
    ('foo/bar/', 'foo/bar/'),
    ('/foo/bar', '/foo/bar'),
    ('/foo/bar/', '/foo/bar/'),
    (1, ''),
)


@pytest.mark.parametrize("url,sanitized_url", urls)
def test_sanitize_url(db, url, sanitized_url):
    assert sanitize_url(url) == sanitized_url
