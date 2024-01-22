import copy
import logging
from collections import defaultdict
from typing import Dict, List, Optional, Sequence

from django.http import HttpRequest

from rdmo.conditions.imports import import_helper_condition
from rdmo.core.imports import (
    check_permissions,
    get_or_return_instance,
    make_import_info_msg,
    set_foreign_field,
    set_lang_field,
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

from .constants import RDMO_MODEL_PATH_MAPPER

logger = logging.getLogger(__name__)


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
        'original': dict,
        'updated_and_changed': dict,
    }


def import_elements(uploaded_elements: List[Dict], save: bool = True, request: Optional[HttpRequest] = None):
    imported_elements = []
    uploaded_uris = {i.get('uri') for i in uploaded_elements}
    for uploaded_element in uploaded_elements:
        element = import_element(element=uploaded_element, save=save, request=request, uploaded_uris=imported_elements)
        element['warnings'] = [val for k, val in element['warnings'].items() if k not in uploaded_uris]
        imported_elements.append(element)
    return imported_elements



def import_element(
        element: Optional[Dict] = None,
        save: bool = True,
        request: Optional[HttpRequest] = None,
        uploaded_uris: Optional[Sequence[str]] = None
    ):

    if element is None:
        return

    model_path = element.get('model')
    if model_path is None:
        return element

    # initialize element dict with default values
    for _k,_val in IMPORT_ELEMENT_INIT_DICT.items():
        element[_k] = _val()

    model = RDMO_MODEL_PATH_MAPPER[model_path]
    user = request.user if request is not None else None
    import_helper = ELEMENT_IMPORT_HELPERS[model_path]
    import_func = import_helper.import_func
    validators = import_helper.validators
    common_fields = import_helper.common_fields
    lang_field_names = import_helper.lang_fields if import_helper.lang_fields is not None else []
    foreign_field_names = import_helper.foreign_fields if import_helper.foreign_fields is not None else []
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
        setattr(instance, common_field, element.get(common_field) or '')
    # set language fields
    for lang_field_name in lang_field_names:
        set_lang_field(instance, lang_field_name, element)
    # set foreign fields
    for foreign_field in foreign_field_names:
        set_foreign_field(instance, foreign_field, element, uploaded_uris=uploaded_uris)

    # call the element specific import method
    instance = import_func(instance, element, validators, save)

    if element.get('errors'):
        return element
    if _updated and not _created:
        element['updated'] = _updated
        # and instance is not original_instance
        # keep only strings, make json serializable
        original_serializer = import_helper.serializer(original_instance, context={'request': request})
        original_data = original_serializer.data
        original_element = {k: val for k,val in original_data.items() if k in element}
        uploaded_serializer = import_helper.serializer(instance, context={'request': request})
        uploaded_data = uploaded_serializer.data
        uploaded_element = {k: val for k,val in uploaded_data.items() if k in original_element}

        updated_and_changed = {}
        for k, old_val in original_element.items():
            new_val = uploaded_element[k]
            if old_val != new_val:
                updated_and_changed[k] = {"current": old_val, "uploaded": new_val}
        # overwrite the "normal" element name with the value from element_uri
        uri_keys = {k for k in list(original_data.keys())+list(uploaded_data.keys())
                    if k.endswith('_uri') or k.endswith('_uris')}
        for uri_key in uri_keys:
            element_name, uri_field = uri_key.split('_')
            if uri_key in updated_and_changed:
                # eg. set attribute as key instead of attribute_uri
                uri_key_val = updated_and_changed[uri_key].pop()
                updated_and_changed[element_name] = uri_key_val
            if element_name in element and uri_key in original_data:
                old_val = original_data[uri_key]
                new_val = element[element_name].get('uri')
                if old_val != new_val:
                    updated_and_changed[element_name] = {"current": old_val, "uploaded": new_val}

        element['updated_and_changed'] = updated_and_changed

    if save:
        logger.info(_msg)
        element['created'] = _created
        element['updated'] = _updated

    return element
