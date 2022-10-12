''' utility methods for the rdmo.catalogs_table app'''

from urllib.parse import urlparse

from django.utils.translation import get_language

from rdmo.core.utils import get_languages

def get_language_field_name(field: str) -> str:
    ''' used for sorting by property of field title_langX '''
    current_language = get_language()
    languages = get_languages()
    if not languages:
        return field
    for lang_code, lang_string, lang_field in languages:
        if lang_code == current_language:
            return f'{field}_{lang_field}'
    return f'{field}_{languages[0][-1]}' # default language at index 0
    