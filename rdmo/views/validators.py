from django.utils.translation import ugettext_lazy as _

from rdmo.core.validators import LockedValidator, UniqueURIValidator

from .models import View


class ViewUniqueURIValidator(UniqueURIValidator):

    model = View

    def get_uri(self, data):
        if data.get('key') is None:
            self.raise_validation_error({'key': _('This field is required.')})
        else:
            uri = self.model.build_uri(data.get('uri_prefix'), data.get('key'))
            return uri


class ViewLockedValidator(LockedValidator):

    pass
