import datetime
from typing import Optional

import pytest

from django.utils.translation import activate

from rdmo.core.utils import (
    human2bytes,
    inject_textblocks,
    join_url,
    parse_date_from_string,
    parse_metadata,
    remove_double_newlines,
    sanitize_url,
)

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

valid_date_strings = [
    ("en", "2025-02-17", datetime.date(2025, 2, 17)),
    ("en", "Feb 17, 2025", datetime.date(2025, 2, 17)),
    ("de", "17.02.2025", datetime.date(2025, 2, 17)),
    ("fr", "17/02/2025", datetime.date(2025, 2, 17)),
    ("nl", "17-02-2025", datetime.date(2025, 2, 17)),
    ("es", "17/02/25", datetime.date(2025, 2, 17)),
]

invalid_date_strings = [
    ("2025-02-31","day is out of range for month"),
    ("2025-17-02", "month must be in 1..12"),
    ("99/99/9999", "Invalid date format"),
    ("abcd-ef-gh", "Invalid date format"),
    ("32-13-2024", "Invalid date format"),
    ("", "Invalid date format"),
    (None, "date must be provided as string"),
    (datetime.date(2025, 2, 17), "date must be provided as string")
]

metadata_html = [
    ('<html><metadata>{"foo": "bar"}</metadata></html>', {'foo': 'bar'}, '<html></html>'),
    ('<html><metadata>{"f</metadata></html>', None, '<html><metadata>{"f</metadata></html>'),
    ('<html></html>', None, '<html></html>')
]

double_newline_strings = [
    ('test\n\n\n\ntest', 'test\n\ntest'),
    ('test\n\n\ntest', 'test\n\ntest'),
    ('test\n\ntest', 'test\n\ntest'),
    ('test\ntest', 'test\ntest'),
]

export_formats = ('xml', 'rtf', 'odt', 'docx', 'html', 'markdown', 'tex', 'pdf')



@pytest.mark.parametrize('url,sanitized_url', urls)
def test_sanitize_url(url, sanitized_url):
    assert sanitize_url(url) == sanitized_url


def test_join_url():
    assert join_url('https://example.com//', '/terms', 'foo') == 'https://example.com/terms/foo'


@pytest.mark.parametrize('human,bytes', human2bytes_test_values)
def test_human2bytes(human: Optional[str], bytes: float):
    assert human2bytes(human) == bytes


@pytest.mark.parametrize("locale, date_string, expected_date", valid_date_strings)
def test_parse_date_from_string_valid_formats(settings, locale, date_string, expected_date):
    activate(locale)
    assert parse_date_from_string(date_string) == expected_date


@pytest.mark.parametrize("invalid_date, error_msg", invalid_date_strings)
def test_parse_date_from_string_invalid_formats(settings, invalid_date, error_msg):
    if not isinstance(invalid_date,str):
        with pytest.raises(TypeError, match=error_msg):
            parse_date_from_string(invalid_date)
    else:
        with pytest.raises(ValueError,match=error_msg):
            parse_date_from_string(invalid_date)


@pytest.mark.parametrize('input_html, metadata, output_html', metadata_html)
def test_parse_metadata(input_html, metadata, output_html):
    assert parse_metadata(input_html) == (metadata, output_html)


@pytest.mark.parametrize('input_string, output_string', double_newline_strings)
def test_remove_double_newlines(input_string, output_string):
    assert remove_double_newlines(input_string) == output_string

