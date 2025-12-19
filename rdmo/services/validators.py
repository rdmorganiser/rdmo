from rest_framework.serializers import ValidationError

from rdmo.config.models import Plugin
from rdmo.config.plugin_type_constants import PluginType


class ProviderValidator:

    def __call__(self, data):
        provider_key = data.get('provider_key')
        plugins = Plugin.objects.for_context(
            plugin_type=PluginType.PROJECT_ISSUE_PROVIDER.value,
            format=provider_key
        )
        provider = plugins.first().initialize_class() if plugins else None
        if provider is None:
            raise ValidationError({
                'provider_key': 'Please provide a valid provider.'
            })

        try:
            options = {option.get('key'): option.get('value') for option in data.get('options', [])}
        except KeyError as e:
            raise ValidationError({
                'options': 'Options need to be of the form "{"key": "": "value": ""}".'
            }) from e

        for key in options:
            if key not in [field.get('key') for field in provider.fields]:
                raise ValidationError({
                    'options': f'Key "{key}" is not valid.'
                })

        for field in provider.fields:
            if field.get('required', True) and field.get('key') not in options:
                raise ValidationError({
                    'options': 'Key "{}" is required.'.format(field.get('key'))
                })
