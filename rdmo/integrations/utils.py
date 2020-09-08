from django.conf import settings

from rdmo.core.utils import import_class


def get_integrations(request):
    integrations = {}
    for key, integration_class_name in settings.INTEGRATIONS:
        integrations[key] = import_class(integration_class_name)(request)
    return integrations


def get_integration(request, integration_key):
    integration_class_name = next(integration_class_name for key, integration_class_name in settings.INTEGRATIONS if key == integration_key)
    if integration_class_name:
        return import_class(integration_class_name)(request)
