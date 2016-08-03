from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from apps.core.models import Model, TranslationMixin
from apps.domain.models import AttributeEntity

from .managers import QuestionEntityManager


@python_2_unicode_compatible
class Catalog(Model, TranslationMixin):

    order = models.IntegerField(null=True)

    title_en = models.CharField(max_length=256)
    title_de = models.CharField(max_length=256)

    class Meta:
        ordering = ('order',)
        verbose_name = _('Catalog')
        verbose_name_plural = _('Catalogs')

    def __str__(self):
        return self.title

    @property
    def title(self):
        return self.trans('title')


@python_2_unicode_compatible
class Section(Model, TranslationMixin):

    catalog = models.ForeignKey(Catalog, related_name='sections')
    order = models.IntegerField(null=True)

    title_en = models.CharField(max_length=256)
    title_de = models.CharField(max_length=256)

    class Meta:
        ordering = ('catalog__order', 'order')
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')

    def __str__(self):
        return '%s / %s' % (self.catalog.title, self.title)

    @property
    def title(self):
        return self.trans('title')


@python_2_unicode_compatible
class Subsection(Model, TranslationMixin):

    section = models.ForeignKey(Section, related_name='subsections')
    order = models.IntegerField(null=True)

    title_en = models.CharField(max_length=256)
    title_de = models.CharField(max_length=256)

    class Meta:
        ordering = ('section__catalog__order', 'section__order', 'order')
        verbose_name = _('Subsection')
        verbose_name_plural = _('Subsections')

    def __str__(self):
        return '%s / %s / %s' % (self.section.catalog.title, self.section.title, self.title)

    @property
    def title(self):
        return self.trans('title')


class QuestionEntity(Model, TranslationMixin):

    objects = QuestionEntityManager()

    attribute_entity = models.ForeignKey(AttributeEntity, blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    subsection = models.ForeignKey('Subsection', related_name='entities')
    order = models.IntegerField(null=True)

    help_en = models.TextField(null=True, blank=True)
    help_de = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('subsection__section__catalog__order', 'subsection__section__order', 'subsection__order', 'order')
        verbose_name = _('QuestionEntity')
        verbose_name_plural = _('QuestionEntities')

    def __str__(self):
        if self.attribute_entity:
            return '%s / %s / %s / %s' % (
                self.subsection.section.catalog.title,
                self.subsection.section.title,
                self.subsection.title,
                self.attribute_entity.title)
        else:
            return '%s / %s / %s / --' % (
                self.subsection.section.catalog.title,
                self.subsection.section.title,
                self.subsection.title
            )

    @property
    def help(self):
        return self.trans('help')

    @property
    def is_collection(self):
        if self.attribute_entity:
            return self.attribute_entity.is_collection
        else:
            return False

    @property
    def is_set(self):
        return not hasattr(self, 'question')


class Question(QuestionEntity):

    WIDGET_TYPE_CHOICES = (
        ('text', 'Text'),
        ('textarea', 'Textarea'),
        ('yesno', 'Yes/No'),
        ('checkbox', 'Checkboxes'),
        ('radio', 'Radio buttons'),
        ('select', 'Select drop-down'),
        ('range', 'Range slider'),
        ('date', 'Date picker'),
    )

    parent = models.ForeignKey('QuestionEntity', blank=True, null=True, related_name='questions')

    text_en = models.TextField()
    text_de = models.TextField()

    widget_type = models.CharField(max_length=12, choices=WIDGET_TYPE_CHOICES)

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

    @property
    def text(self):
        return self.trans('text')
