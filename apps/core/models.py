from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Model(models.Model):

    created = models.DateTimeField(editable=False, verbose_name=_('created'))
    updated = models.DateTimeField(editable=False, verbose_name=_('updated'))

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = now()

        self.updated = now()
        super(Model, self).save(*args, **kwargs)

    class Meta:
        abstract = True
