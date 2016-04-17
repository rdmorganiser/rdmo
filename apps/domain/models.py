from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from apps.core.models import Model


class AttributeEntity(Model):

    tag = models.SlugField()
    is_collection = models.BooleanField()

    class Meta:
        verbose_name = _('AttributeEntity')
        verbose_name_plural = _('AttributeEntities')

    @property
    def is_set(self):
        return hasattr(self, 'attributeset')


@python_2_unicode_compatible
class AttributeSet(AttributeEntity):

    class Meta:
        ordering = ('tag', )
        verbose_name = _('AttributeSet')
        verbose_name_plural = _('AttributeSets')

    def __str__(self):
        return self.tag


@python_2_unicode_compatible
class Attribute(AttributeEntity):

    VALUE_TYPE_TEXT = 'text'
    VALUE_TYPE_INTEGER = 'integer'
    VALUE_TYPE_FLOAT = 'float'
    VALUE_TYPE_BOOLEAN = 'boolean'
    VALUE_TYPE_DATETIME = 'datetime'
    VALUE_TYPE_CHOICES = (
        (VALUE_TYPE_TEXT, _('Text')),
        (VALUE_TYPE_INTEGER, _('Integer')),
        (VALUE_TYPE_FLOAT, _('Float')),
        (VALUE_TYPE_BOOLEAN, _('Boolean')),
        (VALUE_TYPE_DATETIME, _('Datetime'))
    )

    attributeset = models.ForeignKey('AttributeSet', blank=True, null=True, related_name='attributes', help_text='optional')
    value_type = models.CharField(max_length=8, choices=VALUE_TYPE_CHOICES)
    unit = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        ordering = ('attributeset', 'tag', )
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
