from typing import Optional

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

human2bytes_test_values = (
    ("1Gb", 1e+9),
    (None, 0),
    ("0", 0),
)


@pytest.mark.parametrize("url,sanitized_url", urls)
def test_sanitize_url(url, sanitized_url):
    assert sanitize_url(url) == sanitized_url


def test_join_url():
    assert join_url('https://example.com//', '/terms', 'foo') == 'https://example.com/terms/foo'


@pytest.mark.parametrize("human,bytes", human2bytes_test_values)
def test_human2bytes(human: Optional[str], bytes: float):
    assert human2bytes(human) == bytes
