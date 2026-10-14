from django.utils.translation import gettext_lazy as _

from rest_framework.serializers import ValidationError

from rdmo.core.plugins import get_plugin


class ProviderValidator:

    requires_context = True

    def __call__(self, data, serializer):
        provider_key = data.get('provider_key')
        provider = get_plugin('PROJECT_ISSUE_PROVIDERS', provider_key)
        if provider is None:
            raise ValidationError({
                'provider_key': 'Please provide a valid provider.'
            })

        try:
            options_by_key = {option.get('key'): option for option in data.get('options', [])}
        except KeyError as e:
            raise ValidationError({
                'options': 'Options need to be of the form "{"key": "": "value": ""}".'
            }) from e

        for key in options_by_key:
            if key not in [field.get('key') for field in provider.fields]:
                raise ValidationError({
                    'options': f'Key "{key}" is not valid.'
                })

        errors = {}

        for field in provider.fields:
            key = field.get('key')
            option = options_by_key.get(key)
            required = field.get('required', True)

            if option is None:
                has_stored_secret = (
                    serializer.instance
                    and field.get('secret', False)
                    and serializer.instance.get_option_value(key)
                )
                if required and not has_stored_secret:
                    errors[key] = [_('This field is required.')]

            elif not option.get('value'):
                replacing_secret = (
                    serializer.instance
                    and field.get('secret', False)
                    and not option.get('remove')
                )
                if required or replacing_secret:
                    errors[key] = [_('This field may not be blank.')]

        if errors:
            raise ValidationError(errors)
