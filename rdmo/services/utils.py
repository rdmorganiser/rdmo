from django.conf import settings

from rdmo.core.utils import import_class


def get_providers():
    providers = {}
    for key, class_name in settings.SERVICE_PROVIDERS.items():
        providers[key] = import_class(class_name)()
    return providers


def get_provider(provider_key):
    class_name = settings.SERVICE_PROVIDERS.get(provider_key)
    if class_name:
        return import_class(class_name)()
