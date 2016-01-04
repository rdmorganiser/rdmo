from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Permission
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from jsonfield import JSONField


@python_2_unicode_compatible
class Question(models.Model):

    TYPE_CHOICES = (
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

    text_en = models.TextField(blank=True)
    text_de = models.TextField(blank=True)

    type = models.CharField(max_length=11, choices=TYPE_CHOICES)
    options = JSONField(null=True, blank=True, help_text=_('Enter valid JSON of the form [[key, label], [key, label], ...]'))

    previous = models.ForeignKey('Question', null=True, blank=True)

    def __str__(self):
        return '[%s] %s / %s' % (self.identifier, self.text_en, self.text_de)

    class Meta:
        ordering = ('identifier', )
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
