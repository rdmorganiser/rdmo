from __future__ import unicode_literals

from django.core import serializers
from django.core.urlresolvers import reverse
from django.core.exceptions import MultipleObjectsReturned
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language

from jsonfield import JSONField

from apps.core.exceptions import DMPwerkzeugException
from apps.projects.models import Project


class QuestionManager(models.Manager):

    def get_first(self):
        try:
            return self.get(previous=None)
        except MultipleObjectsReturned:
            questions = self.filter(previous=None)
            message = 'More than one question has no previous question (%s).' % ','.join([q.slug for q in questions])
            raise DMPwerkzeugException(message)


@python_2_unicode_compatible
class Interview(models.Model):

    project = models.ForeignKey(Project, related_name='interviews')

    title = models.CharField(max_length=256)

    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = now()

        self.updated = now()
        super(Interview, self).save(*args, **kwargs)

    def __str__(self):
        return '%s - %s' % (self.project.name, self.title)

    class Meta:
        ordering = ('project', 'updated')
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

    objects = QuestionManager()

    identifier = models.CharField(max_length=16)
    slug = models.SlugField()

    text_en = models.TextField(blank=True)
    text_de = models.TextField(blank=True)

    answer_type = models.CharField(max_length=12, choices=ANSWER_TYPE_CHOICES)
    widget_type = models.CharField(max_length=12, choices=WIDGET_TYPE_CHOICES)

    options = JSONField(null=True, blank=True, help_text=_('Enter valid JSON of the form [[key, label], [key, label], ...]'))

    next = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='previous')

    @property
    def text(self):
        if get_language() == 'en':
            return self.text_en
        elif get_language() == 'de':
            return self.text_de
        else:
            raise DMPwerkzeugException('Language is not supported.')

    def __str__(self):
        return '[%s, %s] %s / %s' % (self.identifier, self.slug, self.text_en, self.text_de)

    def get_absolute_url(self):
        return reverse('question', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('identifier', )
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')


@python_2_unicode_compatible
class Answer(models.Model):

    interview = models.ForeignKey('Interview', related_name='answers')
    question = models.ForeignKey('Question')
    value = models.TextField()
    previous_answer = models.ForeignKey('self', null=True)

    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = now()

        self.updated = now()
        super(Answer, self).save(*args, **kwargs)

    def __str__(self):
        return '%s - %s' % (self.interview, self.question.slug)

    class Meta:
        ordering = ('interview', 'question')
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')
