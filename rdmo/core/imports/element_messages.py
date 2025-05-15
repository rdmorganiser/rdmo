from typing import Optional

from rdmo.core.imports.element_changes import ImportElementFields, _initialize_tracking_field


def track_messages_on_element(element: dict,
                              element_field: str,
                              warning: Optional[str] = None,
                              error: Optional[str] = None):
    if warning is not None:
        _initialize_tracking_field(element, element_field)
        _append_warning(element, element_field, warning)
    if error is not None:
        _initialize_tracking_field(element, element_field)
        _append_error(element, element_field, error)


def make_import_info_msg(verbose_name: str, created: bool, uri: Optional[str] = None):
    if uri is None:
        return f"{verbose_name}, no uri"
    if created:
        return f"{verbose_name} created with {uri}"
    return f"{verbose_name} {uri} updated"


def _append_warning(element: dict, element_field: str, warning: str):
    element[ImportElementFields.DIFF][element_field][ImportElementFields.WARNINGS][element['uri']].append(warning)


def _append_error(element: dict, element_field: str, error: str):
    element[ImportElementFields.DIFF][element_field][ImportElementFields.ERRORS].append(error)
