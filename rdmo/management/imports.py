import copy
import logging
from collections import defaultdict
from dataclasses import asdict
from typing import AbstractSet, Dict, List, Optional

from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest

from rdmo.conditions.imports import import_helper_condition
from rdmo.core.imports import (
    check_permissions,
    get_or_return_instance,
    make_import_info_msg,
    set_extra_field,
    set_foreign_field,
    set_lang_field,
    set_m2m_instances,
    set_m2m_through_instances,
    set_reverse_m2m_through_instance,
    validate_instance,
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
from rdmo.questions.utils import get_widget_types
from rdmo.tasks.imports import import_helper_task
from rdmo.views.imports import import_helper_view

logger = logging.getLogger(__name__)


# mapping is redundant, since each ImportHelper has a .model_path attribute
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
        'updated_and_changed': dict,
    }


def import_elements(uploaded_elements: Dict, save: bool = True, request: Optional[HttpRequest] = None) -> List[Dict]:
    imported_elements = []
    uploaded_uris = set(uploaded_elements.keys())
    current_site = get_current_site(request)
    questions_widget_types = get_widget_types()
    for _uri, uploaded_element in uploaded_elements.items():
        element = import_element(element=uploaded_element, save=save, uploaded_uris=uploaded_uris,
                                    request=request, current_site=current_site,
                                    questions_widget_types=questions_widget_types)
        element['warnings'] = {k: val  for k, val in element['warnings'].items() if k not in uploaded_uris}
        imported_elements.append(element)
    return imported_elements



def import_element(
        element: Optional[Dict] = None,
        save: bool = True,
        request: Optional[HttpRequest] = None,
        uploaded_uris: Optional[AbstractSet[str]] = None,
        current_site = None,
        questions_widget_types = None
    ) -> Dict:

    if element is None:
        return {}

    model_path = element.get('model')
    if model_path is None:
        return element

    # initialize element dict with default values
    for _k,_val in IMPORT_ELEMENT_INIT_DICT.items():
        element[_k] = _val()

    user = request.user if request is not None else None
    import_helper = ELEMENT_IMPORT_HELPERS[model_path]
    if import_helper.model_path != model_path:
        raise ValueError(f'Invalid import helper model path: {import_helper.model_path}. Expected {model_path}.')
    model = import_helper.model
    validators = import_helper.validators
    common_fields = import_helper.common_fields
    lang_field_names = import_helper.lang_fields
    foreign_field_names = import_helper.foreign_fields
    extra_field_names = import_helper.extra_fields

    uri = element.get('uri')
    # get or create instance from uri and model_path
    instance, _created = get_or_return_instance(model, uri=uri)

    # keep a copy of the original
    # when the element is updated
    # needs to be created here, else the changes will be overwritten
    original_instance = copy.deepcopy(instance) if not _created else None

    # prepare a log message
    _msg = make_import_info_msg(model._meta.verbose_name, _created, uri=uri)

    # check the change or add permissions for the user on the instance
    _perms_error_msg = check_permissions(instance, uri, user)
    if _perms_error_msg:
        # when there is an error msg, the import could be stopped and return
        element["errors"].append(_perms_error_msg)
        return element

    # prepare original element when updated (maybe rename into lookup)
    _updated = not _created

    # start to set values on the instance
    # set common field values from element on instance
    for common_field in common_fields:
        common_value = element.get(common_field) or ''
        setattr(instance, common_field, common_value)
    strip_uri_prefix_endswith_slash(element)
    ## strip uri_prefix slash for comparison diff
    if original_instance:
        original_instance.uri_prefix = original_instance.uri_prefix.rstrip('/')
    # set language fields
    for lang_field_name in lang_field_names:
        set_lang_field(instance, lang_field_name, element)
    # set foreign fields
    for foreign_field in foreign_field_names:
        set_foreign_field(instance, foreign_field, element, uploaded_uris=uploaded_uris)
    # set extra fields
    for extra_field in extra_field_names:
        set_extra_field(instance, extra_field, element, questions_widget_types=questions_widget_types)
    # call the validators on the instance
    validate_instance(instance, element, *validators)

    if element.get('errors'):
        return element

    if _updated and not _created:
        element['updated'] = _updated
        # and instance is not original_instance
        # keep only strings, make json serializable
        serializer = import_helper.serializer
        changes = get_updated_changes(element, instance, original_instance, serializer, request=request)
        element['updated_and_changed'] = changes

    if save:
        logger.info(_msg)
        element['created'] = _created
        element['updated'] = _updated
        instance.save()
        for m2m_field in import_helper.m2m_instance_fields:
            set_m2m_instances(instance, element, m2m_field)
        for m2m_through_fields in import_helper.m2m_through_instance_fields:
            set_m2m_through_instances(instance, element, **asdict(m2m_through_fields))
        for reverse_m2m_fields in import_helper.reverse_m2m_through_instance_fields:
            set_reverse_m2m_through_instance(instance, element, **asdict(reverse_m2m_fields))

        if import_helper.add_current_site_editors:
            instance.editors.add(current_site)
        if import_helper.add_current_site_sites:
            instance.sites.add(current_site)

    return element

def strip_uri_prefix_endswith_slash(element: dict) -> dict:
    # handle URI Prefix ending with slash
    if 'uri_prefix' not in element:
        return element
    if element['uri_prefix'].endswith('/'):
        element['uri_prefix'] = element['uri_prefix'].rstrip('/')
    return element


def get_updated_changes(element, new_instance,
                        original_instance, serializer, request=None) -> Dict[str, str]:
    original_serializer = serializer(original_instance, context={'request': request})
    original_data = original_serializer.data
    original_element = {k: val for k,val in original_data.items() if k in element}
    uploaded_serializer = serializer(new_instance, context={'request': request})
    uploaded_data = uploaded_serializer.data
    uploaded_element = {k: val for k,val in uploaded_data.items() if k in element}

    updated_and_changed = {}
    for k, old_val in original_element.items():
        new_val = uploaded_element[k]
        if old_val != new_val and any([old_val,new_val]):
            updated_and_changed[k] = {"current": old_val, "uploaded": new_val}
    # overwrite the normal "element" name with the value from "element_uri"
    uri_keys = {k for k in list(original_data.keys())+list(uploaded_data.keys())
                if k.endswith('_uri') or k.endswith('_uris')}
    for uri_key in uri_keys:
        element_name, uri_field = uri_key.split('_')
        if uri_key in updated_and_changed:
            # e.g. set attribute as key instead of attribute_uri
            uri_key_val = updated_and_changed[uri_key].pop()
            updated_and_changed[element_name] = uri_key_val
        if element_name in element and uri_key in original_data:
            old_val = original_data[uri_key]
            new_val = element[element_name].get('uri')
            if old_val != new_val and any([old_val,new_val]):
                updated_and_changed[element_name] = {"current": old_val, "uploaded": new_val}
    return updated_and_changed
