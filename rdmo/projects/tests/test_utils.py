import pytest

from django.http import QueryDict

from ..filters import ProjectFilter
from ..utils import set_context_querystring_with_filter_and_page

GET_queries = [
    'page=2&title=project',
    'page=2',
    'title=project',
    ''
]

@pytest.mark.parametrize('GET_query', GET_queries)
def test_set_context_querystring_with_filter_and_page(GET_query):
    querydict = QueryDict(GET_query)
    filter = ProjectFilter(querydict)
    context = {'filter': filter}
    context = set_context_querystring_with_filter_and_page(context)

    if 'page' in GET_query and 'title' in GET_query:
        assert 'querystring' in context
        assert context['querystring'] == 'title=project'
        querydict_copy = querydict.copy()
        del querydict_copy['page']
        assert context['querystring'] == querydict_copy.urlencode()
    elif 'page' not in GET_query and 'title' in GET_query:
        assert 'querystring' in context
        assert context['querystring'] == 'title=project'
    elif 'page' in GET_query and 'title' not in GET_query:
        assert context.get('querystring', 'not-in-context') == ''
    else:
        assert context.get('querystring', 'not-in-context') == 'not-in-context'
