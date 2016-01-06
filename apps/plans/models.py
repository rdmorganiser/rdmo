from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from apps.interviews.models import Interview


@python_2_unicode_compatible
class Plan(models.Model):

    interview = models.ForeignKey(Interview)
    template = models.ForeignKey('Template')

    def __str__(self):
        return '%s - %s' % (self.interview, self.template)

    class Meta:
        ordering = ('interview', 'template')
        verbose_name = _('Plan')
        verbose_name_plural = _('Plans')


@python_2_unicode_compatible
class Template(models.Model):

    def __str__(self):
        return ''

    class Meta:
        # ordering = ('name', )
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')
