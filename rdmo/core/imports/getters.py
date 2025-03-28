from typing import Optional

from django.db import models

from rdmo.core.constants import RDMO_MODELS
from rdmo.core.utils import get_languages


def get_or_return_instance(model: models.Model, uri: Optional[str] = None) -> tuple[models.Model, bool]:
    if uri is None:
        return model(), True
    try:
        return model.objects.get(uri=uri), False
    except model.DoesNotExist:
        return model(), True
    except model.MultipleObjectsReturned:
        return model.objects.filter(uri=uri).first(), False


def get_rdmo_model_path(target_name: str, field_name: str):
    try:
        return RDMO_MODELS[target_name]
    except KeyError:
        if 'parent' in target_name and 'questionset' in field_name:
            return RDMO_MODELS[field_name]


def get_lang_field_values(field_name: str,
                          element: Optional[dict] = None,
                          instance: Optional[models.Model] = None):
    if element is not None and instance is not None:
        raise ValueError("Please choose one of each")

    ret = []
    for lang_code, lang_verbose_name, lang_field in get_languages():
        name_code = f'{field_name}_{lang_code}'
        name_field = f'{field_name}_{lang_field}'
        row = {}
        row['element_key'] = name_code
        row['instance_field'] = name_field
        if element:
            row['value'] = element.get(name_code, '') or ''
        if instance:
            row['value'] = getattr(instance, name_field, '') or ''
        ret.append(row)
    return ret
