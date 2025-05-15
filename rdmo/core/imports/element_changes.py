from collections import defaultdict
from enum import Enum
from typing import Optional, Union


class ImportElementFields(str, Enum):
    DIFF = "updated_and_changed"
    NEW = "new_data"
    CURRENT = "current_data"
    WARNINGS = "warnings"
    ERRORS = "errors"
    UPDATED = "updated"
    CREATED = "created"
    CHANGED_FIELDS = "changedFields"  # for ignored_keys when ordering at save


def track_changes_m2m_instances(element, field_name,
                                foreign_instances, original=None):
    if original is None:
        return
    original_m2m_instance = getattr(original, field_name)
    original_m2m_instance = original_m2m_instance or []
    # m2m instance fields are unordered so comparison by set
    original_uris = set(original_m2m_instance.values_list('uri', flat=True))
    foreign_uris = {i.uri for i in foreign_instances}
    common_uris = list(original_uris & foreign_uris)
    original_uris_list = common_uris + list(original_uris - foreign_uris)
    foreign_uris_list = common_uris + list(foreign_uris - original_uris)
    track_changes_on_element(element, field_name, new_value=foreign_uris_list,
                             original_value=original_uris_list)


def track_changes_on_uri_of_foreign_field(element, field_name, foreign_uri, original=None):
    if original is None:
        return
    # get foreign uri of original
    original_foreign_instance = getattr(original, field_name, '')
    original_foreign_uri = ''
    if original_foreign_instance:
        original_foreign_uri = getattr(original_foreign_instance, 'uri', '')
    track_changes_on_element(element, field_name, new_value=foreign_uri, original_value=original_foreign_uri)


def _initialize_tracking_field(element: dict, element_field: str):
    if element[ImportElementFields.DIFF].get(element_field) is None:
        element[ImportElementFields.DIFF][element_field] = {
            ImportElementFields.ERRORS: [],
            ImportElementFields.WARNINGS: defaultdict(list)
        }
        return
    if ImportElementFields.ERRORS not in element[ImportElementFields.DIFF][element_field]:
        element[ImportElementFields.DIFF][element_field][ImportElementFields.ERRORS] = []
    if ImportElementFields.WARNINGS not in element[ImportElementFields.DIFF][element_field]:
        element[ImportElementFields.DIFF][element_field][ImportElementFields.WARNINGS] = defaultdict(list)

def _initialize_track_changes_element_field(element: dict, element_field: str) -> None:
    if ImportElementFields.DIFF not in element:
        element[ImportElementFields.DIFF] = {}

    if element_field and element_field not in element[ImportElementFields.DIFF]:
        element[ImportElementFields.DIFF][element_field] = {}


def track_changes_on_element(element: dict,
                             element_field: str,
                             new_value: Union[str, list[str], None] = None,
                             instance_field: Optional[str] = None,
                             original=None,
                             original_value: Optional[Union[str, list[str]]] = None):
    if (original is None and original_value is None) or new_value is None:
        return

    _initialize_track_changes_element_field(element, element_field)

    if original_value is None and original is not None:
        lookup_field = element_field if instance_field is None else instance_field
        original_value = getattr(original, lookup_field, '')

    element[ImportElementFields.DIFF][element_field][ImportElementFields.CURRENT] = original_value
    element[ImportElementFields.DIFF][element_field][ImportElementFields.NEW] = new_value


def track_changes_on_m2m_through_instances(element, field_name, current_data, new_data):
    _initialize_track_changes_element_field(element, field_name)
    element[ImportElementFields.DIFF][field_name][ImportElementFields.NEW] = new_data
    element[ImportElementFields.DIFF][field_name][ImportElementFields.CURRENT] = current_data
    new_values = [i['uri'] for i in new_data]
    original_values = [i['uri'] for i in current_data]
    track_changes_on_element(element, field_name, new_value=new_values, original_value=original_values)
