import copy
import logging
from typing import AbstractSet, Dict, List, Optional

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest

from rdmo.core.imports import (
    check_permissions,
    get_or_return_instance,
    make_import_info_msg,
    validate_instance,
)
from rdmo.management.import_utils import (
    ELEMENT_IMPORT_HELPERS,
    add_current_site_to_sites_and_editor,
    apply_field_values,
    initialize_import_element_dict,
    strip_uri_prefix_endswith_slash,
    update_related_fields,
)

logger = logging.getLogger(__name__)


def import_elements(uploaded_elements: Dict, save: bool = True, request: Optional[HttpRequest] = None) -> List[Dict]:
    imported_elements = []
    uploaded_uris = set(uploaded_elements.keys())
    current_site = get_current_site(request)
    for _uri, uploaded_element in uploaded_elements.items():
        element = import_element(element=uploaded_element,
                                 save=save,
                                 uploaded_uris=uploaded_uris,
                                 request=request,
                                 current_site=current_site)
        element['warnings'] = {k: val for k, val in element['warnings'].items() if k not in uploaded_uris}
        imported_elements.append(element)
    return imported_elements


def import_element(
        element: Optional[Dict] = None,
        save: bool = True,
        request: Optional[HttpRequest] = None,
        uploaded_uris: Optional[AbstractSet[str]] = None,
        current_site = None
    ) -> Dict:

    if element is None:
        return {}

    model_path = element.get('model')
    if model_path is None:
        return element

    initialize_import_element_dict(element)

    user = request.user if request is not None else None
    import_helper = ELEMENT_IMPORT_HELPERS[model_path]
    if import_helper.model_path != model_path:
        raise ValueError(f'Invalid import helper model path: {import_helper.model_path}. Expected {model_path}.')
    model = import_helper.model
    validators = import_helper.validators

    uri = element.get('uri')
    # get or create instance from uri and model_path
    instance, created = get_or_return_instance(model, uri=uri)

    # keep a copy of the original
    # when the element is updated
    # needs to be created here, else the changes will be overwritten
    original = copy.deepcopy(instance) if not created else None

    # prepare a log message
    msg = make_import_info_msg(model._meta.verbose_name, created, uri=uri)

    # check the change or add permissions for the user on the instance
    perms_error_msg = check_permissions(instance, uri, user)
    if perms_error_msg:
        # when there is an error msg, the import can be stopped and return
        element["errors"].append(perms_error_msg)
        return element

    updated = not created
    element['created'] = created
    element['updated'] = updated
    # INFO: the dict element[FieldNames.diff.value] is filled by calling track_changes_on_element

    element = strip_uri_prefix_endswith_slash(element)
    # start to set values on the instance
    apply_field_values(instance, element, import_helper, uploaded_uris, original)

    # call the validators on the instance
    validate_instance(instance, element, *validators)

    if element.get('errors'):
        # when there is an error msg, the import can be stopped and return
        return element

    if save:
        logger.info(msg)
        instance.save()

    if save or updated:
        update_related_fields(instance, element, import_helper, original, save)

    if save and settings.MULTISITE:
        add_current_site_to_sites_and_editor(instance, current_site, import_helper)

    return element
