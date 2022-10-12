from netrc import netrc
import pytest 

from rdmo.catalogs_table.utils import get_language_field_name

from django.utils.translation import get_language

from rdmo.core.utils import get_languages

languages = ['de', 'en', 'fr']

fields = ['title']   

lang_field_names = ['title_lang1', 'title_lang2', 'title_lang3']

@pytest.mark.parametrize("fields", lang_field_names)
def test_get_language_field_name(field):
    assert get_language_field_name(field) in lang_field_names
