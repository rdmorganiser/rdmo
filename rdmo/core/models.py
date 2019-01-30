from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language

from rdmo.core.exceptions import RDMOException
from rdmo.core.constants import LANGUAGE_RANGE


class Model(models.Model):

    created = models.DateTimeField(editable=False, verbose_name=_('created'))
    updated = models.DateTimeField(editable=False, verbose_name=_('updated'))

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id or kwargs.get('force_insert', False):
            self.created = now()

        self.updated = now()
        super(Model, self).save(*args, **kwargs)


class TranslationMixin(object):

    def trans(self, field):
        current_language = get_language()

        for i in LANGUAGE_RANGE:
            try:
                lang_code, lang = settings.LANGUAGES[i]

                if lang_code == current_language:
                    return getattr(self, '%s_lang%i' % (field, i + 1))

            except IndexError:
                break

        raise RDMOException('Language is not supported.')
