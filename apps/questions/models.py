from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
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
        return self.label

    @property
    def title(self):
        return self.trans('title')

    @property
    def label(self):
        return self.trans('title')


def post_save_catalog(sender, **kwargs):
    instance = kwargs['instance']

    for section in instance.sections.all():
        section.save()

post_save.connect(post_save_catalog, sender=Catalog)


@python_2_unicode_compatible
class Section(Model, TranslationMixin):

    catalog = models.ForeignKey(Catalog, related_name='sections')
    order = models.IntegerField(null=True)

    title_en = models.CharField(max_length=256)
    title_de = models.CharField(max_length=256)

    label_de = models.TextField()
    label_en = models.TextField()

    class Meta:
        ordering = ('catalog__order', 'order')
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')

    def __str__(self):
        return self.label

    @property
    def title(self):
        return self.trans('title')

    @property
    def label(self):
        return self.trans('label')


def post_save_section(sender, **kwargs):
    instance = kwargs['instance']
    instance.label_en = instance.catalog.title_en + ' / ' + instance.title_en
    instance.label_de = instance.catalog.title_de + ' / ' + instance.title_de

    post_save.disconnect(post_save_section, sender=sender)
    instance.save()
    post_save.connect(post_save_section, sender=sender)

    for subsection in instance.subsections.all():
        subsection.save()

post_save.connect(post_save_section, sender=Section)


@python_2_unicode_compatible
class Subsection(Model, TranslationMixin):

    section = models.ForeignKey(Section, related_name='subsections')
    order = models.IntegerField(null=True)

    title_en = models.CharField(max_length=256)
    title_de = models.CharField(max_length=256)

    label_de = models.TextField()
    label_en = models.TextField()

    class Meta:
        ordering = ('section__catalog__order', 'section__order', 'order')
        verbose_name = _('Subsection')
        verbose_name_plural = _('Subsections')

    def __str__(self):
        return self.label

    @property
    def title(self):
        return self.trans('title')

    @property
    def label(self):
        return self.trans('label')


def post_save_subsection(sender, **kwargs):
    instance = kwargs['instance']
    instance.label_en = instance.section.label_en + ' / ' + instance.title_en
    instance.label_de = instance.section.label_de + ' / ' + instance.title_de

    post_save.disconnect(post_save_subsection, sender=sender)
    instance.save()
    post_save.connect(post_save_subsection, sender=sender)

    for entity in instance.entities.all():
        entity.save()


post_save.connect(post_save_subsection, sender=Subsection)


class QuestionEntity(Model, TranslationMixin):

    objects = QuestionEntityManager()

    attribute_entity = models.ForeignKey(AttributeEntity, blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    subsection = models.ForeignKey('Subsection', related_name='entities')
    order = models.IntegerField(null=True)

    label_de = models.TextField()
    label_en = models.TextField()

    help_en = models.TextField(null=True, blank=True)
    help_de = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('subsection__section__catalog__order', 'subsection__section__order', 'subsection__order', 'order')
        verbose_name = _('QuestionEntity')
        verbose_name_plural = _('QuestionEntities')

    def __str__(self):
        return self.label

    @property
    def help(self):
        return self.trans('help')

    @property
    def label(self):
        return self.trans('label')

    @property
    def is_collection(self):
        if self.attribute_entity:
            return self.attribute_entity.is_collection
        else:
            return False

    @property
    def is_set(self):
        return not hasattr(self, 'question')


def post_save_question_entity(sender, **kwargs):
    instance = kwargs['instance']

    if instance.attribute_entity:
        instance.label_en = instance.subsection.label_en + ' / ' + instance.attribute_entity.title
        instance.label_de = instance.subsection.label_de + ' / ' + instance.attribute_entity.title
    else:
        instance.label_en = instance.subsection.label_en + ' / --'
        instance.label_de = instance.subsection.label_de + ' / --'

    post_save.disconnect(post_save_question_entity, sender=sender)
    instance.save()
    post_save.connect(post_save_question_entity, sender=sender)


post_save.connect(post_save_question_entity, sender=QuestionEntity)


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
