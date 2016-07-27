from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from apps.core.models import TranslationMixin
from apps.conditions.models import Condition


@python_2_unicode_compatible
class AttributeEntity(models.Model):

    parent_entity = models.ForeignKey('AttributeEntity', blank=True, null=True, related_name='children', help_text='optional')

    title = models.CharField(max_length=256)
    full_title = models.CharField(max_length=2048, db_index=True)

    description = models.TextField(blank=True, null=True)
    uri = models.URLField(blank=True, null=True)

    is_collection = models.BooleanField(default=False)

    parent_collection = models.ForeignKey('AttributeEntity', blank=True, null=True, default=None, related_name='+', db_index=True)

    conditions = models.ManyToManyField(Condition, blank=True)

    class Meta:
        ordering = ('full_title', )
        verbose_name = _('AttributeEntity')
        verbose_name_plural = _('AttributeEntities')

    def __str__(self):
        return self.full_title

    @property
    def is_attribute(self):
        return hasattr(self, 'attribute')

    @property
    def range(self):
        if self.is_attribute:
            return self.attribute.range
        else:
            return None

    @property
    def has_options(self):
        if self.is_attribute:
            return bool(self.attribute.options.all())
        else:
            return False

    @property
    def has_conditions(self):
        return bool(self.conditions.all())


@python_2_unicode_compatible
class Attribute(AttributeEntity):

    VALUE_TYPE_TEXT = 'text'
    VALUE_TYPE_INTEGER = 'integer'
    VALUE_TYPE_FLOAT = 'float'
    VALUE_TYPE_BOOLEAN = 'boolean'
    VALUE_TYPE_DATETIME = 'datetime'
    VALUE_TYPE_OPTIONS = 'options'
    VALUE_TYPE_CHOICES = (
        (VALUE_TYPE_TEXT, _('Text')),
        (VALUE_TYPE_INTEGER, _('Integer')),
        (VALUE_TYPE_FLOAT, _('Float')),
        (VALUE_TYPE_BOOLEAN, _('Boolean')),
        (VALUE_TYPE_DATETIME, _('Datetime')),
        (VALUE_TYPE_OPTIONS, _('Options'))
    )

    value_type = models.CharField(max_length=8, choices=VALUE_TYPE_CHOICES)
    unit = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        verbose_name = _('Attribute')
        verbose_name_plural = _('Attributes')

    def __str__(self):
        return self.full_title


def post_save_attribute_entity(sender, **kwargs):
    instance = kwargs['instance']

    # init fields
    instance.full_title = instance.title

    # set parent_collection if the entity is a collection itself
    if instance.is_collection and not instance.is_attribute:
        instance.parent_collection = instance

    # loop over parents
    parent = instance.parent_entity
    while parent:
        # set parent_collection if it is not yet set and if parent is a collection
        if not instance.parent_collection and parent.is_collection:
            instance.parent_collection = parent

        # update own full name
        instance.full_title = parent.title + '.' + instance.full_title

        parent = parent.parent_entity

    post_save.disconnect(post_save_attribute_entity, sender=sender)
    instance.save()
    post_save.connect(post_save_attribute_entity, sender=sender)

    # update the full name and parent_collection of children
    # this makes it recursive
    for child in instance.children.all():
        child.save()


post_save.connect(post_save_attribute_entity, sender=AttributeEntity)
post_save.connect(post_save_attribute_entity, sender=Attribute)


@python_2_unicode_compatible
class VerboseName(models.Model, TranslationMixin):

    attribute_entity = models.OneToOneField('AttributeEntity')

    name_en = models.CharField(max_length=256)
    name_de = models.CharField(max_length=256)

    name_plural_en = models.CharField(max_length=256)
    name_plural_de = models.CharField(max_length=256)

    class Meta:
        verbose_name = _('VerboseName')
        verbose_name_plural = _('VerboseNames')

    def __str__(self):
        return self.attribute_entity.full_title

    @property
    def name(self):
        return self.trans('name')

    @property
    def name_plural(self):
        return self.trans('name_plural')


@python_2_unicode_compatible
class Option(models.Model, TranslationMixin):

    attribute = models.ForeignKey('Attribute', related_name='options')

    order = models.IntegerField(null=True)

    text_en = models.CharField(max_length=256)
    text_de = models.CharField(max_length=256)

    additional_input = models.BooleanField(default=False)

    class Meta:
        ordering = ('attribute', 'order', )
        verbose_name = _('Option')
        verbose_name_plural = _('Options')

    def __str__(self):
        return '%s / %s' % (self.attribute.full_title, self.text)

    @property
    def text(self):
        return self.trans('text')


@python_2_unicode_compatible
class Range(models.Model, TranslationMixin):

    attribute = models.OneToOneField('Attribute')

    minimum = models.FloatField()
    maximum = models.FloatField()
    step = models.FloatField()

    class Meta:
        ordering = ('attribute', )
        verbose_name = _('Range')
        verbose_name_plural = _('Ranges')

    def __str__(self):
        return self.attribute.full_title
