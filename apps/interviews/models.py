from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Permission
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from jsonfield import JSONField

from apps.projects.models import Project


@python_2_unicode_compatible
class Interview(models.Model):

    project = models.ForeignKey(Project)

    title = models.CharField(max_length=256)
    date = models.DateField()

    def __str__(self):
        return '%s - %s' % (self.project.name, self.title)

    class Meta:
        ordering = ('project', 'date')
        verbose_name = _('Interview')
        verbose_name_plural = _('Interviews')


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
        ('checkbox', 'Checkbox'),
        ('radio', 'Radio button'),
        ('select', 'Select'),
        ('multiselect', 'Multiselect'),
        ('slider', 'Slider'),
        ('list', 'List'),
    )

    identifier = models.CharField(max_length=16)
    slug = models.SlugField()

    text_en = models.TextField(blank=True)
    text_de = models.TextField(blank=True)

    answer_type = models.CharField(max_length=12, choices=ANSWER_TYPE_CHOICES)
    widget_type = models.CharField(max_length=12, choices=WIDGET_TYPE_CHOICES)

    options = JSONField(null=True, blank=True, help_text=_('Enter valid JSON of the form [[key, label], [key, label], ...]'))

    previous = models.ForeignKey('Question', null=True, blank=True)

    def __str__(self):
        return '[%s, %s] %s / %s' % (self.identifier, self.slug, self.text_en, self.text_de)

    class Meta:
        ordering = ('identifier', )
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')


@python_2_unicode_compatible
class Answer(models.Model):

    interview = models.ForeignKey('Interview')
    question = models.ForeignKey('Question')

    answer = models.TextField()

    def __str__(self):
        return '%s - %s' % (self.interview, self.question.tag)

    class Meta:
        ordering = ('interview', 'question')
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')
