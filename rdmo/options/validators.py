from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from rdmo.core.validators import UniqueKeyValidator, UniquePathValidator


class OptionSetUniqueKeyValidator(UniqueKeyValidator):

    app_label = 'options'
    model_name = 'optionset'


class OptionUniquePathValidator(UniquePathValidator):

    app_label = 'options'
    model_name = 'option'

    def get_path(self, model, data):
        if 'key' not in data:
            raise ValidationError({
                'key': _('This field is required')
            })
        elif 'optionset' not in data:
            raise ValidationError({
                'optionset': _('This field is required')
            })
        else:
            return model.build_path(data['key'], data['optionset'])
