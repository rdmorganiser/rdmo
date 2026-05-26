from rest_framework.serializers import ValidationError

from rdmo.config.constants import PLUGIN_TYPES


class ProviderValidator:

    def __call__(self, data):
        plugin = data.get('plugin')
        provider = plugin.initialize_class() if plugin else None
        if provider is None or plugin.plugin_type != PLUGIN_TYPES.PROJECT_ISSUE_PROVIDER:
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
