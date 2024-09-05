import copy
import logging
from collections import OrderedDict
from typing import Dict, List, Optional

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest

from rdmo.conditions.imports import import_helper_condition
from rdmo.core.imports import (
    ImportElementFields,
    check_permissions,
    get_or_return_instance,
    make_import_info_msg,
    validate_instance,
)
from rdmo.core.xml import order_elements
from rdmo.domain.imports import import_helper_attribute
from rdmo.management.import_utils import (
    add_current_site_to_sites_and_editor,
    apply_field_values,
    initialize_and_clean_import_element_dict,
    initialize_import_element_dict,
    is_valid_import_element,
    strip_uri_prefix_endswith_slash,
    update_extra_fields_from_validated_instance,
    update_related_fields,
)
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
    "domain.attribute": import_helper_attribute,
    "options.option": import_helper_option,
    "conditions.condition": import_helper_condition,
    "options.optionset": import_helper_optionset,
    "questions.question": import_helper_question,
    "questions.questionset": import_helper_questionset,
    "questions.section": import_helper_section,
    "questions.page": import_helper_page,
    "questions.catalog": import_helper_catalog,
    "tasks.task": import_helper_task,
    "views.view": import_helper_view
}


def import_elements(uploaded_elements: OrderedDict,
                    save: bool = True,
                    request: Optional[HttpRequest] = None) -> List[Dict]:
    imported_elements = []
    uploaded_elements_initial_ordering = {uri: n for n, uri in enumerate(uploaded_elements.keys())}
    uploaded_uris = set(uploaded_elements.keys())
    current_site = get_current_site(request)
    if save:
        # when saving, the elements are ordered according to the rdmo models
        pass
        uploaded_elements = order_elements(uploaded_elements)

    for _uri, uploaded_element in uploaded_elements.items():
        if not is_valid_import_element(uploaded_element):
            continue
        element = import_element(
            element=uploaded_element,
            save=save,
            request=request,
            current_site=current_site
        )
        element[ImportElementFields.WARNINGS] = {
            k: val for
            k, val in element[ImportElementFields.WARNINGS].items()
            if k not in uploaded_uris
        }
        imported_elements.append(element)

    # sort elements back to initial order of uploaded elements
    imported_elements = sorted(
        imported_elements,
        key=lambda x: uploaded_elements_initial_ordering.get(x['uri'],
        float('inf'))
    )

    return imported_elements


def import_element(
        element: Optional[Dict] = None,
        save: bool = True,
        request: Optional[HttpRequest] = None,
        current_site = None
    ) -> Dict:

    initialize_import_element_dict(element)

    import_helper = ELEMENT_IMPORT_HELPERS[element['model']]

    uri = element.get('uri')

    element, _excluded_data = initialize_and_clean_import_element_dict(element, import_helper.model)

    # get or create instance from uri and model
    instance, created = get_or_return_instance(import_helper.model, uri=uri)

    # keep a copy of the original
    # when the element is updated
    # needs to be created here, else the changes will be overwritten
    original = copy.deepcopy(instance) if not created else None

    # prepare a log message
    msg = make_import_info_msg(import_helper.model._meta.verbose_name, created, uri=uri)

    # check the change or add permissions for the user on the instance
    user = request.user if request is not None else None
    perms_error_msg = check_permissions(instance, uri, user)
    if perms_error_msg:
        # when there is an error msg, the import can be stopped and return
        element[ImportElementFields.ERRORS].append(perms_error_msg)
        return element

    element[ImportElementFields.CREATED] = created
    element[ImportElementFields.UPDATED] = not created and original is not None
    # INFO: the dict element[FieldNames.diff.value] is filled by calling track_changes_on_element

    element = strip_uri_prefix_endswith_slash(element)
    # start to set values on the instance
    apply_field_values(instance, element, import_helper, original)

    # call the validators on the instance
    validate_instance(instance, element, *import_helper.validators)

    update_extra_fields_from_validated_instance(instance, element, import_helper, original=original)

    if element.get(ImportElementFields.ERRORS):
        # when there is an error msg, the import can be stopped and return
        if save:
            element[ImportElementFields.CREATED] = False
            element[ImportElementFields.UPDATED] = False
        return element

    if save:
        logger.info(msg)
        instance.save()

        update_related_fields(instance, element, import_helper, original, save)

        if created and settings.MULTISITE:
            add_current_site_to_sites_and_editor(instance, current_site, import_helper)

    elif not created:  # when an element will be updated but not saved
        update_related_fields(instance, element, import_helper, original, save)

    return element
