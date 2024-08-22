import logging
from collections import defaultdict
from dataclasses import asdict
from typing import Dict, Set, Tuple

from django.core.exceptions import FieldDoesNotExist
from django.db.models import Model

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from rdmo.core.imports import (
    ImportElementFields,
    set_common_fields,
    set_extra_field,
    set_foreign_field,
    set_lang_field,
    set_m2m_instances,
    set_m2m_through_instances,
    set_reverse_m2m_through_instance,
    track_changes_on_element,
)

logger = logging.getLogger(__name__)

IMPORT_ELEMENT_INIT_DICT = {
        ImportElementFields.WARNINGS: lambda: defaultdict(list),
        ImportElementFields.ERRORS: list,
        ImportElementFields.CREATED: bool,
        ImportElementFields.UPDATED: bool,
        ImportElementFields.DIFF: dict,
    }


def is_valid_import_element(element: dict) -> bool:
    if element is None or not isinstance(element, dict):
        return False
    if not all(i in element for i in ['model', 'uri']):
        return False
    return True


def get_redundant_keys_from_element(element_keys: Set, model: Model) -> Set:
    model_fields = {i.name for i in model._meta.get_fields()}
    required_element_keys = {'uri', 'model'}
    import_dict_keys = {i.value for i in IMPORT_ELEMENT_INIT_DICT.keys()}
    redundant_keys = element_keys - model_fields - required_element_keys - import_dict_keys

    lang_fields_prefix = {i.split('_lang')[0] for i in model_fields if 'lang' in i}
    element_lang_keys = {i for i in element_keys if any(i.startswith(a) for a in lang_fields_prefix)}
    redundant_keys = redundant_keys - element_lang_keys
    return redundant_keys

def initialize_import_element_dict(element: Dict) -> None:
    # initialize element dict with default values
    for _k,_val in IMPORT_ELEMENT_INIT_DICT.items():
        element[_k] = _val()
    return element


def initialize_and_clean_import_element_dict(element: Dict, model: Model) -> Tuple[Dict, Dict]:
    redundant_keys = get_redundant_keys_from_element(set(element.keys()), model)
    excluded_element_data = {}
    for k in redundant_keys:
        excluded_element_data[k] = element.pop(k)
    # initialize element dict with default values
    element = initialize_import_element_dict(element)
    return element, excluded_element_data


def strip_uri_prefix_endswith_slash(element: dict) -> dict:
    """Removes the trailing slash from the URI prefix if it exists."""
    if 'uri_prefix' in element and element['uri_prefix'].endswith('/'):
        element['uri_prefix'] = element['uri_prefix'].rstrip('/')
    return element


def apply_field_values(instance, element, import_helper, original) -> None:
    """Applies the field values from the element to the instance."""
    # start to set values on the instance
    # set common field values from element on instance
    for field in import_helper.common_fields:
        set_common_fields(instance, field, element, original=original)
    # set language fields
    for field in import_helper.lang_fields:
        set_lang_field(instance, field, element, original=original)
    # set foreign fields
    for field in import_helper.foreign_fields:
        set_foreign_field(instance, field, element, original=original)
    # set extra fields, track changes is done after instance.full_clean
    for extra_field in import_helper.extra_fields:
        set_extra_field(instance, extra_field.field_name, element,
                        extra_field_helper=extra_field)


def validate_with_serializer_field(instance, field_name, value):
    """Validate and convert a value using the corresponding DRF serializer field."""

    # Ensure the field exists on the model
    try:
        model_field = instance._meta.get_field(field_name)
    except FieldDoesNotExist:
        logger.debug("Field '%s' does not exist on the model.", field_name)
        return None

    # Use ModelSerializer's field building logic
    serializer = ModelSerializer(instance=instance)
    try:
        field_class, field_kwargs = serializer.build_standard_field(field_name, model_field)
    except (KeyError, AttributeError):
        logger.info("Could not build a field for '%s'.", field_name)
        return None

    # Handle None values and null fields
    if value is None and field_kwargs.get('allow_null', False):
        return value  # None is allowed, no need to validate further

    try:
        # Instantiate the field with the kwargs and run validation
        drf_field = field_class(**field_kwargs)
        return drf_field.run_validation(value)
    except ValidationError as e:
        # Log only if the value is truly invalid
        if value is not None:
            logger.info("Cannot convert '%s' for field '%s' using '%s': %s",
                         value, field_name, field_class.__name__, str(e))
    return None


def update_extra_fields_from_validated_instance(instance, element, import_helper, original=None) -> None:

    for extra_field in import_helper.extra_fields:
        field_name = extra_field.field_name

        element_field_value = element.get(field_name)

        # deserialize the element value by using the drf field serializer
        validated_value = validate_with_serializer_field(instance, field_name, element_field_value)

        if validated_value is not None:
            element[field_name] = validated_value

        # track changes
        track_changes_on_element(element, field_name, new_value=element[field_name], original=original)


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
