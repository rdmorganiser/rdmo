''' utility methods for the rdmo.catalogs_table app'''

from urllib.parse import urlparse

from django.utils.translation import get_language

from rdmo.core.utils import get_languages


def split_and_break_long_uri(uri: str, maxwidth: int= 12) -> str:
    ''' takes an uri_prefix and adds html breaks <br> when it is too long'''

    if not uri:
        return ''

    parsed_uri = urlparse(uri)

    netloc_split = parsed_uri.netloc.split('.')

    if len(parsed_uri.netloc) > maxwidth or len(netloc_split) >= 2:
        
        split_groups = split_groups_up_to_maxwidth(netloc_split, maxwidth)
        html_uri_prefix_netloc = join_groups_with_break(split_groups)
    else:
        html_uri_prefix_netloc = parsed_uri.netloc
    
    html_uri_prefix_wbreak = html_uri_prefix_netloc + '<br>' + parsed_uri.path 

    return html_uri_prefix_wbreak

def split_groups_up_to_maxwidth(netloc_split: list, maxwidth: int) -> list:
    ''' splits a list of strings in groups with len up to maxwidth '''
    
    groups, grp = [], []
    for el in netloc_split:
        
        if len(el) >= maxwidth:
            groups.append([el])
            grp = []
            continue
        
        grp.append(el)
        
        len_grp = sum(map(len, grp))
        
        if len_grp >= maxwidth:
            groups.append(grp)
            grp = []
    
    if not groups and grp:
        groups.append(grp)
        
    return groups

def join_groups_with_break(groups):
    return "<br>.".join([".".join(i) for i in groups])

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
    