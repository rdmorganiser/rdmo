from types import SimpleNamespace

import pytest

from django.test import RequestFactory
from django.utils import translation

from rdmo.core.filters import SearchFilter


class DummyQuerySet:

    def filter(self, q):
        self.q = q
        return self


@pytest.mark.parametrize('language,search', [
    ('en-us', 'English title'),
    ('de-at', 'Deutscher Title'),
])
def test_search_filter_uses_base_language_for_regional_locale(settings, language, search):
    settings.LANGUAGES = (
        ('en', 'English'),
        ('de', 'German'),
    )
    request = RequestFactory().get('/', {'search': search})
    queryset = DummyQuerySet()
    view = SimpleNamespace(detail=False, search_fields=('title',))

    with translation.override(language):
        SearchFilter().filter_queryset(request, queryset, view)

    assert queryset.q.children == [(f'title_lang{1 if language == "en-us" else 2}__contains', search)]


def test_search_filter_prefers_exact_regional_locale(settings):
    settings.LANGUAGES = (
        ('en', 'English'),
        ('en-GB', 'English (GB)'),
        ('de', 'German'),
    )
    request = RequestFactory().get('/', {'search': 'British title'})
    queryset = DummyQuerySet()
    view = SimpleNamespace(detail=False, search_fields=('title',))

    with translation.override('en-gb'):
        SearchFilter().filter_queryset(request, queryset, view)

    assert queryset.q.children == [('title_lang2__contains', 'British title')]
