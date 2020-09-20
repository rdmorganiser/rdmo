from django.conf import settings
from rdmo.core.utils import import_class


def get_providers():
    providers = {}
    for key, class_name in settings.SERVICE_PROVIDERS:
        providers[key] = import_class(class_name)()
    return providers


def get_provider(provider_key):
    try:
        key, class_name = next((key, class_name) for key, class_name in settings.SERVICE_PROVIDERS if key == provider_key)
        return import_class(class_name)()
    except StopIteration:
        return None
