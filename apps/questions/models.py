from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language

from apps.core.exceptions import DMPwerkzeugException


@python_2_unicode_compatible
class Section(models.Model):

    slug = models.SlugField()
    order = models.IntegerField(null=True)

    title_en = models.CharField(max_length=256)
    title_de = models.CharField(max_length=256)

    @property
    def title(self):
        if get_language() == 'en':
            return self.title_en
        elif get_language() == 'de':
            return self.title_de
        else:
            raise DMPwerkzeugException('Language is not supported.')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('order',)
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')


@python_2_unicode_compatible
class Subsection(models.Model):

    slug = models.SlugField()
    order = models.IntegerField(null=True)

    title_en = models.CharField(max_length=256)
    title_de = models.CharField(max_length=256)

    section = models.ForeignKey(Section, related_name='subsections')

    @property
    def title(self):
        if get_language() == 'en':
            return self.title_en
        elif get_language() == 'de':
            return self.title_de
        else:
            raise DMPwerkzeugException('Language is not supported.')

    @property
    def section_slug(self):
        return self.section.slug

    @property
    def section_title(self):
        return self.section.title

    def __str__(self):
        return '%s / %s' % (self.section_title, self.title)

    class Meta:
        ordering = ('section__order', 'order')
        verbose_name = _('Subsection')
        verbose_name_plural = _('Subsections')


class GroupManager(models.Manager):

    def get_next(self, last_group):
        groups = self \
            .filter(order__gte=last_group.order) \
            .filter(subsection__order__gte=last_group.subsection.order) \
            .filter(subsection__section__order__gte=last_group.subsection.section.order)

        for i, group in enumerate(groups):
            if group == last_group:
                print (i, len(groups))
                if i + 1 >= len(groups):
                    raise Group.DoesNotExist
                else:
                    return groups[i + 1]


@python_2_unicode_compatible
class Group(models.Model):

    objects = GroupManager()

    slug = models.SlugField()
    order = models.IntegerField(null=True)

    title_en = models.CharField(max_length=256)
    title_de = models.CharField(max_length=256)

    subsection = models.ForeignKey(Subsection, related_name='groups')

    @property
    def title(self):
        if get_language() == 'en':
            return self.title_en
        elif get_language() == 'de':
            return self.title_de
        else:
            raise DMPwerkzeugException('Language is not supported.')

    @property
    def section_slug(self):
        return self.subsection.section.slug

    @property
    def section_title(self):
        return self.subsection.section.title

    @property
    def subsection_slug(self):
        return self.subsection.slug

    @property
    def subsection_title(self):
        return self.subsection.title

    def __str__(self):
        return '%s / %s / %s' % (self.section_title, self.subsection_title, self.title)

    class Meta:
        ordering = ('subsection__section__order', 'subsection__order',  'order',)
        verbose_name = _('Group')
        verbose_name_plural = _('Group')


@python_2_unicode_compatible
class Question(models.Model):

    ANSWER_TYPE_CHOICES = (
        ('bool', 'Bool'),
        ('string', 'String'),
        ('list', 'List'),
        ('integer', 'Integer'),
        ('float', 'Float')
    )

    WIDGET_TYPE_CHOICES = (
        ('text', 'Text'),
        ('textarea', 'Textarea'),
        ('yesno', 'Yes/No'),
        ('checkbox', 'Checkboxes'),
        ('radio', 'Radio buttons'),
        ('select', 'Select'),
        ('multiselect', 'Multiselect'),
        ('slider', 'Slider'),
        ('list', 'List'),
    )

    slug = models.SlugField()
    order = models.IntegerField(null=True)

    group = models.ForeignKey(Group, related_name='questions')

    text_en = models.TextField()
    text_de = models.TextField()

    answer_type = models.CharField(max_length=12, choices=ANSWER_TYPE_CHOICES)
    widget_type = models.CharField(max_length=12, choices=WIDGET_TYPE_CHOICES)

    options = models.ManyToManyField('Option', blank=True)

    @property
    def text(self):
        if get_language() == 'en':
            return self.text_en
        elif get_language() == 'de':
            return self.text_de
        else:
            raise DMPwerkzeugException('Language is not supported.')

    @property
    def section_slug(self):
        return self.group.subsection.section.slug

    @property
    def section_title(self):
        return self.group.subsection.section.title

    @property
    def subsection_slug(self):
        return self.group.subsection.slug

    @property
    def subsection_title(self):
        return self.group.subsection.title

    @property
    def group_slug(self):
        return self.group.slug

    @property
    def group_title(self):
        return self.group.title

    def __str__(self):
        return '%s / %s / %s / %s' % (self.section_title, self.subsection_title, self.group_title, self.text)

    class Meta:
        ordering = ('group__subsection__section__order', 'group__subsection__order',  'group__order', 'order')
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')


@python_2_unicode_compatible
class Option(models.Model):

    key = models.SlugField()

    text_en = models.CharField(max_length=256)
    text_de = models.CharField(max_length=256)

    @property
    def text(self):
        if get_language() == 'en':
            return self.text_en
        elif get_language() == 'de':
            return self.text_de
        else:
            raise DMPwerkzeugException('Language is not supported.')

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('key', )
        verbose_name = _('Option')
        verbose_name_plural = _('Options')


@python_2_unicode_compatible
class Condition(models.Model):

    RELATION_CHOICES = (
        ('>', 'greater (>)'),
        ('>=', 'greater equal (>=)'),
        ('<', 'lesser (<)'),
        ('<=', 'lesser equal (<=)'),
        ('==', 'equal (==)'),
        ('!=', 'not equal (!=)'),
    )

    group = models.ForeignKey(Group, related_name='conditions')

    question = models.ForeignKey(Question)
    relation = models.CharField(max_length=2, choices=RELATION_CHOICES)
    value = models.CharField(max_length=256)

    def __str__(self):
        return self.group.title

    class Meta:
        # ordering = ('condition_question', 'condition_value')
        verbose_name = _('Condition')
        verbose_name_plural = _('Conditions')
