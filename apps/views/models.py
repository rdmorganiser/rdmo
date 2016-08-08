from __future__ import unicode_literals

from django.db import models

from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class View(models.Model):

    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('View')
        verbose_name_plural = _('Views')

    def __str__(self):
        return self.title
