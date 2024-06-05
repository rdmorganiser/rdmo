from collections import defaultdict
from dataclasses import asdict
from typing import Dict

from rdmo.conditions.imports import import_helper_condition
from rdmo.core.imports import (
    ELEMENT_DIFF_FIELD_NAME,
    set_extra_field,
    set_foreign_field,
    set_lang_field,
    set_m2m_instances,
    set_m2m_through_instances,
    set_reverse_m2m_through_instance,
    track_changes_on_element,
)
from rdmo.domain.imports import import_helper_attribute
from rdmo.options.imports import import_helper_option, import_helper_optionset
from rdmo.questions.imports import (
    import_helper_catalog,
    import_helper_page,
    import_helper_question,
    import_helper_questionset,
    import_helper_section,
)
from rdmo.tasks.imports import import_helper_task
from rdmo.views.imports import import_helper_view

ELEMENT_IMPORT_HELPERS = {
    "conditions.condition": import_helper_condition,
    "domain.attribute": import_helper_attribute,
    "options.optionset": import_helper_optionset,
    "options.option": import_helper_option,
    "questions.catalog": import_helper_catalog,
    "questions.section": import_helper_section,
    "questions.page": import_helper_page,
    "questions.questionset": import_helper_questionset,
    "questions.question": import_helper_question,
    "tasks.task": import_helper_task,
    "views.view": import_helper_view
}
IMPORT_ELEMENT_INIT_DICT = {
        'warnings': lambda: defaultdict(list),
        'errors': list,
        'created': bool,
        'updated': bool,
        ELEMENT_DIFF_FIELD_NAME: dict,
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
        value = element.get(field) or ''
        setattr(instance, field, value)
        if element['updated']:
            # track changes for common fields
            track_changes_on_element(element, field, new_value=value, original=original)
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
