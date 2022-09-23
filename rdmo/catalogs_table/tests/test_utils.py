from netrc import netrc
import pytest 

# from ..utils import wrap_uri, split_groups_up_to_width, wrap_long_string, get_language_field_name
from ..utils import parse_sort_query

width = 14


uri_prefixes = [
    '',
    123,
    'http://example.com/terms',
    'http://super.long.and.complicated123.uri-prefix.com/terms',
    'https://rdmorganiser.github.io/terms',
    'https://40a23bbff2ca45daa3b2e6a2bbc02a44a362396d.rdmo',
    ]
# [(uri, wrap_uri(uri)) for uri in uri_prefixes]
wrapped_uris = [
    ('', ''),
    (123, ''),
    ('http://example.com/terms', 'example.com<br>/terms'),
    ('http://super.long.and.complicated123.uri-prefix.com/terms',
    'super.long.and<br>.complicated123<br>.uri-prefix.com<br>/terms'),
    ('https://rdmorganiser.github.io/terms',
    'rdmorganiser.github<br>.io<br>/terms'),
    ('https://40a23bbff2ca45daa3b2e6a2bbc02a44a362396d.rdmo',
    '40a23bbff2ca45<br>daa3b2e6a2bbc0<br>2a44a362396d<br>.rdmo<br>')
    ]

# [(urlparse(str(uri)).netloc, split_groups_up_to_width(urlparse(str(uri)).netloc, width)) for uri in uri_prefixes]

uri_netlocs =[
 ('', [['']]),
 ('example.com', [['example', 'com']]),
 ('super.long.and.complicated123.uri-prefix.com',
  [['super', 'long', 'and'], ['complicated123'], ['uri-prefix', 'com']]),
 ('rdmorganiser.github.io', [['rdmorganiser', 'github'], ['io']]),
 ('40a23bbff2ca45daa3b2e6a2bbc02a44a362396d.rdmo',
  [['40a23bbff2ca45<br>daa3b2e6a2bbc0<br>2a44a362396d'], ['rdmo']])
  ]

sort_query_str = 'sort=id'
uri_sort_queries = [(str(i)+'?'+sort_query_str, sort_query_str ) for i in uri_prefixes]

@pytest.mark.parametrize("uri,sort_query", uri_sort_queries)
def test_parse_sort_query(uri, sort_query):
    assert parse_sort_query(uri) == sort_query


def _remove():
    @pytest.mark.parametrize("uri,wrapped_uri", wrapped_uris)
    def test_wrap_uris(uri, wrapped_uri):
        assert wrap_uri(uri, width=width) == wrapped_uri

    @pytest.mark.parametrize("uri_netloc,split_netloc", uri_netlocs)
    def test_split_netloc_uris(uri_netloc, split_netloc):
        assert split_groups_up_to_width(uri_netloc, width=width) == split_netloc