from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language

from rdmo.core.exceptions import RDMOException


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

        if get_language() == 'en':
            return getattr(self, field + '_en')
        elif get_language() == 'de':
            return getattr(self, field + '_de')
        else:
            raise RDMOException('Language is not supported.')
