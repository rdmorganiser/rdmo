from django import forms

from rdmo.options.providers import Provider


class SimpleOptionSetProvider(Provider):
    default_uri_prefix = "https://rdmorganiser.github.io/terms"
    refresh = True
    settings_namespace = 'SIMPLE_OPTIONSET_PROVIDER'

    class SettingsForm(forms.Form):
        PROVIDER_LABEL = forms.CharField(required=False, initial='Simple answer 1')

    settings_form_class = SettingsForm

    def get_options(self, project, search=None, user=None, site=None):
        return [
            {
                'id': 'simple_1',
                'text': self.settings.PROVIDER_LABEL,
                'help': 'One'
            },
            {
                'id': 'simple_2',
                'text': 'Simple answer 2',
                'help': 'Two'
            },
            {
                'id': 'simple_3',
                'text': 'Simple answer 3',
                'help': 'Three'
            }
        ]
