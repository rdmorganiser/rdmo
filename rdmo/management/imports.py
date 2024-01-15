import copy
import logging
from collections import defaultdict
from typing import Dict, List, Optional, Sequence

from django.db import models
from django.forms.models import model_to_dict

from rdmo.conditions.imports import import_helper_condition
from rdmo.core.imports import (
    check_permissions,
    get_lang_field_values,
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
        'warnings': defaultdict(list),
        'errors': [],
        'created': False,
        'updated': False,
        'original': defaultdict(),
        'updated_and_changed': defaultdict(),
    }


def import_elements(uploaded_elements: List[Dict], save: bool = True, user: Optional[models.Model] = None):
    imported_elements = []
    uploaded_uris = {i.get('uri') for i in uploaded_elements}
    for element in uploaded_elements:
        element = import_element(element=element, save=save, user=user, uploaded_uris=imported_elements)
        # replace warnings with filtered list of warnings
        warnings = element.pop('warnings')
        element['warnings'] = filter_warnings(warnings, uploaded_uris)
        imported_elements.append(element)
    return imported_elements


def filter_warnings(warnings: Dict, uploaded_uris: List[Dict]) -> List[str]:
    # remove warnings regarding elements which are in the elements list
    ret = []
    if not warnings:
        return ret
    for uri, messages in warnings.items():
        if uri not in uploaded_uris:
            ret += messages
    return ret


def import_element(
        element: Optional[Dict] = None,
        save: bool = True,
        user: Optional[models.Model] = None,
        uploaded_uris: Optional[Sequence[str]] = None
    ):

    if element is None:
        return element

    model_path = element.get('model')
    if model_path is None:
        return element

    # initialize element dict with default values
    element.update(IMPORT_ELEMENT_INIT_DICT)

    model = RDMO_MODEL_PATH_MAPPER[model_path]
    import_helper = ELEMENT_IMPORT_HELPERS[model_path]
    import_method = import_helper.import_method
    validators = import_helper.validators
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
    original_element = {}
    filtered_ffnames = filter(lambda x: x in original_element, foreign_field_names)
    if _updated:
        original_element = model_to_dict(original_instance)
        original_element = {k: original_element.get(k, element.get(k))
                            for k in element.keys() if k not in IMPORT_ELEMENT_INIT_DICT}
        for _field in filtered_ffnames:
            if original_element[_field] is None:
                continue
            try:
                # set the uri for foreign fields, instead of id
                original_element[_field] = {'uri': getattr(original_instance, _field).uri}
            except AttributeError:
                pass
    # start to set values on the instance
    # set common field values from element on instance
    for common_field in import_helper.common_fields:
        setattr(instance, common_field, element.get(common_field) or '')
    # set language fields
    for lang_field_name in lang_field_names:
        set_lang_field(instance, lang_field_name, element)
        if original_instance is not None:
            # add the lang_code fields from the original instance
            lang_field_values = get_lang_field_values(lang_field_name, instance=original_instance)
            original_element.update(lang_field_values)
    # set foreign fields
    for foreign_field in foreign_field_names:
        set_foreign_field(instance, foreign_field, element, uploaded_uris=uploaded_uris)

    # call the element specific import method
    instance = import_method(instance, element, validators, save)

    if element.get('errors'):
        return element

    if _updated and not _created:
        element['updated'] = _updated
        # and instance is not original_instance
        # keep only strings, make json serializable
        original_element_json = {k: val for k, val in original_element.items() if isinstance(val, str)}
        element['original'] = original_element_json
        # add updated and changed
        instance_field_names = {i.name for i in instance._meta.local_concrete_fields}
        updated_and_changed = {}
        for k, val in filter(lambda x: x[0] in instance_field_names, original_element.items()):

            new_val = getattr(instance, k, None)
            if k in foreign_field_names and new_val is not None:
                try:
                    # set the uri for foreign fields, instead of id
                    new_val = {'uri': getattr(instance, k).uri}
                except AttributeError:
                    pass

            if new_val is None:
                continue
            if new_val != val:
                updated_and_changed[k] = {"current": val, "uploaded": new_val}

        element['updated_and_changed'] = updated_and_changed

    if save:
        logger.info(_msg)
        element['created'] = _created
        element['updated'] = _updated

    return element
