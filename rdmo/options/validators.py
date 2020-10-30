from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from rdmo.core.validators import UniqueURIValidator


class OptionSetUniqueURIValidator(UniqueURIValidator):

    app_label = 'options'
    model_name = 'optionset'

    def get_uri(self, model, data):
        uri = model.build_uri(data.get('uri_prefix'), data.get('key'))
        return uri


class OptionUniqueURIValidator(UniqueURIValidator):

    app_label = 'options'
    model_name = 'option'

    def get_uri(self, model, data):
        if 'key' not in data:
            raise ValidationError({
                'key': _('This field is required')
            })
        elif 'optionset' not in data:
            raise ValidationError({
                'optionset': _('This field is required')
            })
        else:
            path = model.build_path(data.get('key'), data.get('optionset'))
            uri = model.build_uri(data.get('uri_prefix'), path)
            return uri
