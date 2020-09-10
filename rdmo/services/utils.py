from django.conf import settings

from rdmo.core.utils import import_class


def get_providers(request):
    providers = {}
    for key, class_name in settings.SERVICE_PROVIDERS:
        providers[key] = import_class(class_name)(request)
    return providers


def get_provider(request, provider_key):
    class_name = next(class_name for key, class_name in settings.SERVICE_PROVIDERS if key == provider_key)
    if class_name:
        return import_class(class_name)(request)
