import logging

from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from rdmo.core.utils import get_languages

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
        current_language = (get_language() or '').lower()
        languages = {
            lang_code.lower(): lang_field
            for lang_code, _lang_string, lang_field in get_languages()
        }

        exact_lang_field = languages.get(current_language)
        if exact_lang_field:
            r = getattr(self, f'{field}_{exact_lang_field}') or None
            if r is not None:
                return r
        else:
            base_language = current_language.split('-')[0]
            base_lang_field = languages.get(base_language)
            if base_lang_field:
                r = getattr(self, f'{field}_{base_lang_field}') or None
                if r is not None:
                    return r

        if settings.REPLACE_MISSING_TRANSLATION:
            for i in range(1, 6):
                r = getattr(self, '{}_{}'.format(field, 'lang' + str(i))) or None
                if r is not None:
                    return r
        return ''
