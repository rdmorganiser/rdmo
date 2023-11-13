import logging
from collections import defaultdict
from typing import Optional

from django.forms.models import model_to_dict

from rdmo.conditions.imports import import_helper_condition
from rdmo.core.imports import common_import_methods, get_lang_field_values, set_lang_field
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
        'errors': None,
        'created': False,
        'updated': False,
        'original': defaultdict()
    }


def import_elements(uploaded_elements, save=True, user=None):
    imported_elements = []
    for element in uploaded_elements:
        model = element.get('model')
        if model is None:
            continue
        element = import_element(model_path=model, element=element, save=save, user=user)
        element = filter_warnings(element, uploaded_elements)
        imported_elements.append(element)
    return imported_elements


def filter_warnings(element, elements):
    # remove warnings regarding elements which are in the elements list
    warnings = []
    for uri, messages in element['warnings'].items():
        if not next(filter(lambda e: e['uri'] == uri, elements), None):
            warnings += messages

    element['warnings'] = warnings
    return element


def import_element(
        model_path: Optional[str] = None,
        element: Optional[dict] = None,
        save: bool = True,
        user = None
    ):

    if element is None:
        return element

    element.update(IMPORT_ELEMENT_INIT_DICT)
    element['errors'] = []

    if model_path is None:
        return element

    import_helper = ELEMENT_IMPORT_HELPERS[model_path]
    import_method = import_helper.import_method
    model_path = import_helper.dotted_path
    validators = import_helper.validators
    lang_field_names = import_helper.lang_fields
    uri = element.get('uri')

    instance, _msg, _created, original_instance = common_import_methods(
                            model_path,
                            uri=uri
                    )
    # prepare original element when updated (maybe rename into lookup)
    _updated = not _created
    original_element = {}
    if _updated:
        original_element = model_to_dict(original_instance)
        original_element = {k: original_element.get(k, element.get(k))
                            for k in element.keys() if k not in IMPORT_ELEMENT_INIT_DICT}
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
    # call the element specific import method
    instance = import_method(instance, element, validators, save, user)

    if element.get('errors'):
        return element

    if _updated:
        element['updated'] = _updated
        # make json serializable, keep only strings
        original_element_json = {k: val for k, val in original_element.items() if isinstance(val, str)}
        element['original'] = original_element_json

    if save:
        logger.info(_msg)
        element['created'] = _created
        element['updated'] = _updated

    return element
