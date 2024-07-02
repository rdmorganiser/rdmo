from collections import defaultdict
from dataclasses import asdict
from typing import Dict

from rdmo.core.imports import (
    ImportElementFields,
    set_common_fields,
    set_extra_field,
    set_foreign_field,
    set_lang_field,
    set_m2m_instances,
    set_m2m_through_instances,
    set_reverse_m2m_through_instance,
)

IMPORT_ELEMENT_INIT_DICT = {
        ImportElementFields.WARNINGS: lambda: defaultdict(list),
        ImportElementFields.ERRORS: list,
        ImportElementFields.CREATED: bool,
        ImportElementFields.UPDATED: bool,
        ImportElementFields.DIFF: dict,
    }


def initialize_import_element_dict(element: Dict) -> None:
    # initialize element dict with default values
    for _k,_val in IMPORT_ELEMENT_INIT_DICT.items():
        element[_k] = _val()


def strip_uri_prefix_endswith_slash(element: dict) -> dict:
    """Removes the trailing slash from the URI prefix if it exists."""
    if 'uri_prefix' in element and element['uri_prefix'].endswith('/'):
        element['uri_prefix'] = element['uri_prefix'].rstrip('/')
    return element


def apply_field_values(instance, element, import_helper, uploaded_uris, original) -> None:
    """Applies the field values from the element to the instance."""
    element = strip_uri_prefix_endswith_slash(element)
    # start to set values on the instance
    # set common field values from element on instance
    for field in import_helper.common_fields:
        set_common_fields(instance, field, element, original=original)
    # set language fields
    for field in import_helper.lang_fields:
        set_lang_field(instance, field, element, original=original)
    # set foreign fields
    for field in import_helper.foreign_fields:
        set_foreign_field(instance, field, element, uploaded_uris=uploaded_uris, original=original)

    for extra_field in import_helper.extra_fields:
        set_extra_field(instance, extra_field.field_name, element, extra_field_helper=extra_field, original=original)


def update_related_fields(instance, element, import_helper, original, save) -> None:
    # this part updates the related fields of the instance
    for m2m_field in import_helper.m2m_instance_fields:
        set_m2m_instances(instance, element, m2m_field, original=original, save=save)
    for m2m_through_fields in import_helper.m2m_through_instance_fields:
        set_m2m_through_instances(instance, element, **asdict(m2m_through_fields),
                                  original=original, save=save)
    for reverse_m2m_fields in import_helper.reverse_m2m_through_instance_fields:
        set_reverse_m2m_through_instance(instance, element, **asdict(reverse_m2m_fields),
                                         original=original, save=save)


def add_current_site_to_sites_and_editor(instance, current_site, import_helper):
    if import_helper.add_current_site_editors:
        instance.editors.add(current_site)
    if import_helper.add_current_site_sites:
        instance.sites.add(current_site)
