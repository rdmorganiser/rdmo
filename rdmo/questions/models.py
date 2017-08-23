from __future__ import unicode_literals

from django.core.cache import caches
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from rdmo.core.utils import get_uri_prefix
from rdmo.core.models import Model, TranslationMixin
from rdmo.domain.models import AttributeEntity

from .managers import QuestionEntityManager
from .validators import (
    CatalogUniqueKeyValidator,
    SectionUniquePathValidator,
    SubsectionUniquePathValidator,
    QuestionEntityUniquePathValidator,
    QuestionUniquePathValidator
)


@python_2_unicode_compatible
class Catalog(Model, TranslationMixin):

    uri = models.URLField(
        max_length=640, blank=True, null=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this catalog (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256, blank=True, null=True,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this catalog.')
    )
    key = models.SlugField(
        max_length=128, blank=True, null=True,
        verbose_name=_('Key'),
        help_text=_('The internal identifier of this catalog.')
    )
    comment = models.TextField(
        blank=True, null=True,
        verbose_name=_('Comment'),
        help_text=_('Additional internal information about this catalog.')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('The position of this catalog in lists.')
    )
    title_en = models.CharField(
        max_length=256,
        verbose_name=_('Title (en)'),
        help_text=_('The English title for this catalog.')
    )
    title_de = models.CharField(
        max_length=256,
        verbose_name=_('Title (de)'),
        help_text=_('The German title for this catalog.')
    )

    class Meta:
        ordering = ('order',)
        verbose_name = _('Catalog')
        verbose_name_plural = _('Catalogs')
        permissions = (('view_catalog', 'Can view Catalog'),)

    def __str__(self):
        return self.uri or self.key

    def save(self, *args, **kwargs):
        self.uri = get_uri_prefix(self) + '/questions/%s' % self.key
        super(Catalog, self).save(*args, **kwargs)

        for section in self.sections.all():
            section.save()

    def clean(self):
        CatalogUniqueKeyValidator(self)()

    @property
    def title(self):
        return self.trans('title')


@python_2_unicode_compatible
class Section(Model, TranslationMixin):

    uri = models.URLField(
        max_length=640, blank=True, null=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this section (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256, blank=True, null=True,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this section.')
    )
    key = models.SlugField(
        max_length=128, blank=True, null=True,
        verbose_name=_('Key'),
        help_text=_('The internal identifier of this section.')
    )
    path = models.CharField(
        max_length=512, blank=True, null=True,
        verbose_name=_('Label'),
        help_text=_('The path part of the URI of this section (auto-generated).')
    )
    comment = models.TextField(
        blank=True, null=True,
        verbose_name=_('Comment'),
        help_text=_('Additional internal information about this section.')
    )
    catalog = models.ForeignKey(
        Catalog, related_name='sections',
        verbose_name=_('Catalog'),
        help_text=_('The catalog this section belongs to.')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('Position in lists.')
    )
    title_en = models.CharField(
        max_length=256,
        verbose_name=_('Title (en)'),
        help_text=_('The English title for this section.')
    )
    title_de = models.CharField(
        max_length=256,
        verbose_name=_('Title (de)'),
        help_text=_('The German title for this section.')
    )

    class Meta:
        ordering = ('catalog__order', 'order')
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')
        permissions = (('view_section', 'Can view Section'),)

    def __str__(self):
        return self.uri or self.key

    def save(self, *args, **kwargs):
        self.path = Section.build_path(self.key, self.catalog)
        self.uri = get_uri_prefix(self) + '/questions/' + self.path

        super(Section, self).save(*args, **kwargs)

        for subsection in self.subsections.all():
            subsection.save()

    def clean(self):
        self.path = Section.build_path(self.key, self.catalog)
        SectionUniquePathValidator(self)()

    @property
    def title(self):
        return self.trans('title')

    @classmethod
    def build_path(cls, key, catalog):
        return '%s/%s' % (catalog.key, key)


@python_2_unicode_compatible
class Subsection(Model, TranslationMixin):

    uri = models.URLField(
        max_length=640, blank=True, null=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this subsection (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256, blank=True, null=True,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this subsection.')
    )
    key = models.SlugField(
        max_length=128, blank=True, null=True,
        verbose_name=_('Key'),
        help_text=_('The internal identifier of this subsection.')
    )
    path = models.CharField(
        max_length=512, blank=True, null=True,
        verbose_name=_('Label'),
        help_text=_('The path part of the URI of this subsection (auto-generated).')
    )
    comment = models.TextField(
        blank=True, null=True,
        verbose_name=_('Comment'),
        help_text=_('Additional internal information about this subsection.')
    )
    section = models.ForeignKey(
        Section, related_name='subsections',
        verbose_name=_('Section'),
        help_text=_('The section this subsection belongs to.')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('Position in lists.')
    )
    title_en = models.CharField(
        max_length=256,
        verbose_name=_('Title (en)'),
        help_text=_('The English title for this subsection.')
    )
    title_de = models.CharField(
        max_length=256,
        verbose_name=_('Title (de)'),
        help_text=_('The German title for this subsection.')
    )

    class Meta:
        ordering = ('section__catalog__order', 'section__order', 'order')
        verbose_name = _('Subsection')
        verbose_name_plural = _('Subsections')
        permissions = (('view_subsection', 'Can view Subsection'),)

    def __str__(self):
        return self.uri or self.key

    def save(self, *args, **kwargs):
        self.path = Subsection.build_path(self.key, self.section)
        self.uri = get_uri_prefix(self) + '/questions/' + self.path

        super(Subsection, self).save(*args, **kwargs)

        for entity in self.entities.all():
            entity.save()

    def clean(self):
        self.path = Subsection.build_path(self.key, self.section)
        SubsectionUniquePathValidator(self)()

    @property
    def title(self):
        return self.trans('title')

    @classmethod
    def build_path(cls, key, section):
        return '%s/%s/%s' % (section.catalog.key, section.key, key)


class QuestionEntity(Model, TranslationMixin):

    objects = QuestionEntityManager()

    uri = models.URLField(
        max_length=640, blank=True, null=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this question/questionset (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256, blank=True, null=True,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this question/questionset.')
    )
    key = models.SlugField(
        max_length=128, blank=True, null=True,
        verbose_name=_('Key'),
        help_text=_('The internal identifier of this question/questionset.')
    )
    path = models.CharField(
        max_length=512, blank=True, null=True,
        verbose_name=_('Path'),
        help_text=_('The path part of the URI of this question/questionset (auto-generated).')
    )
    comment = models.TextField(
        blank=True, null=True,
        verbose_name=_('Comment'),
        help_text=_('Additional internal information about this question/questionset.')
    )
    attribute_entity = models.ForeignKey(
        AttributeEntity, blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
        verbose_name=_('Attribute entity'),
        help_text=_('The attribute/entity this question/questionset belongs to.')
    )
    subsection = models.ForeignKey(
        Subsection, related_name='entities',
        verbose_name=_('Subsection'),
        help_text=_('The subsection this question/questionset belongs to.')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('The position of this question/questionset in lists.')
    )
    help_en = models.TextField(
        null=True, blank=True,
        verbose_name=_('Help (en)'),
        help_text=_('The English help text for this question/questionset.')
    )
    help_de = models.TextField(
        null=True, blank=True,
        verbose_name=_('Help (de)'),
        help_text=_('The German help text for this question/questionset.')
    )

    class Meta:
        ordering = ('subsection__section__catalog__order', 'subsection__section__order', 'subsection__order', 'order')
        verbose_name = _('Question entity')
        verbose_name_plural = _('Question entities')
        permissions = (('view_questionentity', 'Can view Question entity'),)

    def __str__(self):
        return self.uri or self.key

    def save(self, *args, **kwargs):
        try:
            self.path = QuestionEntity.build_path(self.key, self.subsection, self.parent)
        except AttributeError:
            self.path = QuestionEntity.build_path(self.key, self.subsection)

        self.uri = get_uri_prefix(self) + '/questions/' + self.path

        super(QuestionEntity, self).save(*args, **kwargs)

        for question in self.questions.all():
            question.save()

        # invalidate the cache so that changes appear instantly
        caches['api'].clear()

    def clean(self):
        try:
            self.path = QuestionEntity.build_path(self.key, self.subsection, self.parent)
            QuestionUniquePathValidator(self)()
        except AttributeError:
            self.path = QuestionEntity.build_path(self.key, self.subsection)
            QuestionEntityUniquePathValidator(self)()

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

    @classmethod
    def build_path(cls, key, subsection, questionset=None):
        if questionset:
            return '%s/%s/%s/%s/%s' % (
                subsection.section.catalog.key,
                subsection.section.key,
                subsection.key,
                questionset.key,
                key
            )
        else:
            return '%s/%s/%s/%s' % (
                subsection.section.catalog.key,
                subsection.section.key,
                subsection.key,
                key
            )


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

    parent = models.ForeignKey(
        QuestionEntity, blank=True, null=True, related_name='questions',
        verbose_name=_('Parent'),
        help_text=_('The question set this question belongs to.')
    )
    text_en = models.TextField(
        verbose_name=_('Text (en)'),
        help_text=_('The English text for this question.')
    )
    text_de = models.TextField(
        verbose_name=_('Text (de)'),
        help_text=_('The German text for this question.')
    )
    widget_type = models.CharField(
        max_length=12, choices=WIDGET_TYPE_CHOICES,
        verbose_name=_('Widget type'),
        help_text=_('Type of widget for this question.')
    )

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
        permissions = (('view_question', 'Can view Question'),)

    @property
    def text(self):
        return self.trans('text')
