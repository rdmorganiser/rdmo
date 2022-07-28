''' utility methods for the rdmo.catalogs_table app'''

import textwrap

from urllib.parse import urlparse

from django.utils.translation import get_language

from rdmo.core.utils import get_languages

#  wrap_uri, split_groups_up_to_width, wrap_long_string, get_language_field_name
def parse_sort_query(url: str):
    query = urlparse(url).query
    if not query:
        return ''
    if not 'sort' in query:
        return ''
    return query

def wrap_uri(uri: str, width: int= 14) -> str:
    ''' takes an uri_prefix and adds html breaks <br> when it is too long'''

    if not uri:
        return ''

    if not type(uri) == str:
        return ''
    
    parsed_uri = urlparse(uri)
    netloc = parsed_uri.netloc

    if len(netloc) > width:
        split_groups = split_groups_up_to_width(netloc, width)
        html_uri_prefix_netloc = "<br>.".join([".".join(i) for i in split_groups])
        # join_groups_with_break(split_groups)
    else:
        html_uri_prefix_netloc = netloc
    
    html_uri_prefix_wbreak = html_uri_prefix_netloc + '<br>' + parsed_uri.path 

    return html_uri_prefix_wbreak

def split_groups_up_to_width(netloc: str, width: int= 14, split_str: str= '.') -> list:
    ''' splits a list of strings in groups with len up to maxwidth '''

    netloc_split = netloc.split(split_str)
    groups, grp = [], []
    for el in netloc_split:
        
        if len(el) >= width:
            if grp:
                groups.append(grp)
            groups.append([wrap_long_string(el, width= width)])
            grp = []
            continue
        
        grp.append(el)
        
        len_grp = sum(map(len, grp))
        
        if len_grp >= width:
            groups.append(grp)
            grp = []
    
    if grp:
        groups.append(grp)
        
    return groups

def wrap_long_string(el: str, width: int= None, join_str: str= "<br>") -> str:
    
    if not width:
        return el

    if len(el) < width:
        return el
    
    return join_str.join(textwrap.wrap(el, width))


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
    