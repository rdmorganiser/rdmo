import logging

from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from rdmo.core.utils import get_current_language_field

logger = logging.getLogger(__name__)


class Model(models.Model):

    created = models.DateTimeField(editable=False, verbose_name=_('created'))
    updated = models.DateTimeField(editable=False, verbose_name=_('updated'))

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.created is None:
            self.created = now()

        self.updated = now()

        super().save(*args, **kwargs)


class TranslationMixin:

    def trans(self, field):
        lang_field = get_current_language_field()
        if lang_field:
            r = getattr(self, f'{field}_{lang_field}') or None
            if r is not None:
                return r

        if settings.REPLACE_MISSING_TRANSLATION:
            for i in range(1, 6):
                r = getattr(self, '{}_{}'.format(field, 'lang' + str(i))) or None
                if r is not None:
                    return r
        return ''
