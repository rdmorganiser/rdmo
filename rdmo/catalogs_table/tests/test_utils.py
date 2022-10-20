import pytest 

from ..utils import get_language_field_name

from django.utils.translation import activate


language_field_test = [
    ('en', 'title', 'title_lang1'),
    ('de', 'title', 'title_lang2'),
    ('test', 'title', 'title_lang1'),
    ('', 'title', 'title_lang1'),
    ]

@pytest.mark.parametrize("lang, field, lang_field", language_field_test)
def test_get_language_field_name(lang, field, lang_field):
    activate(lang)
    assert get_language_field_name(field) == lang_field
