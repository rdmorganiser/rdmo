from django.conf import settings
from rdmo.core.utils import import_class


def get_providers():
    providers = {}
    for key, label, class_name in settings.OPTIONSET_PROVIDERS:
        providers[key] = import_class(class_name)(key, label, class_name)
    return providers


def get_provider(provider_key):
    try:
        key, label, class_name = next(
            (key, label, class_name) for key, label, class_name in settings.OPTIONSET_PROVIDERS if key == provider_key
        )
        return import_class(class_name)(key, label, class_name)
    except StopIteration:
        return None
