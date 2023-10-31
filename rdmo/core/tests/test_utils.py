import pytest

from rdmo.core.utils import human2bytes, join_url, sanitize_url

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
def test_sanitize_url(url, sanitized_url):
    assert sanitize_url(url) == sanitized_url


def test_join_url():
    assert join_url('https://example.com//', '/terms', 'foo') == 'https://example.com/terms/foo'


def test_human2bytes():
    assert human2bytes('1Gb') == 1e+9


def test_human2bytes_none():
    assert human2bytes(None) == 0


def test_human2bytes_zero():
    assert human2bytes('0') == 0
