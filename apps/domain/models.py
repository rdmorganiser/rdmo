from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from apps.core.models import Model


@python_2_unicode_compatible
class AttributeSet(Model):

    tag = models.SlugField()

    class Meta:
        verbose_name = _('AttributeSet')
        verbose_name_plural = _('AttributeSets')

    def __str__(self):
        return self.tag


@python_2_unicode_compatible
class Attribute(Model):

    tag = models.SlugField()

    attributeset = models.ForeignKey('AttributeSet', blank=True, null=True, related_name='attributes')

    class Meta:
        verbose_name = _('Attribute')
        verbose_name_plural = _('Attributes')

    def __str__(self):
        if self.attributeset:
            return self.attributeset.tag + '.' + self.tag
        else:
            return self.tag


@python_2_unicode_compatible
class Template(Model):

    def __str__(self):
        return ''

    class Meta:
        # ordering = ('name', )
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')
