from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from rdmo.core.models import TranslationMixin


class ProxyUser(User):

    class Meta:
        proxy = True
        default_permissions = ()
        permissions = (('view_user', 'Can view user'),)


@python_2_unicode_compatible
class AdditionalField(models.Model, TranslationMixin):

    TYPE_CHOICES = (
        ('text', 'Text'),
        ('textarea', 'Textarea'),
    )

    key = models.SlugField()
    type = models.CharField(max_length=11, choices=TYPE_CHOICES)

    text_en = models.CharField(max_length=256)
    text_de = models.CharField(max_length=256)

    help_en = models.TextField(null=True, blank=True, help_text=_('Enter a help text to be displayed next to the input element'))
    help_de = models.TextField(null=True, blank=True, help_text=_('Enter a help text to be displayed next to the input element'))

    required = models.BooleanField()

    class Meta:
        ordering = ('key',)

        verbose_name = _('Additional field')
        verbose_name_plural = _('Additional fields')

    def __str__(self):
        return self.text

    @property
    def text(self):
        return self.trans('text')

    @property
    def help(self):
        return self.trans('help')


@python_2_unicode_compatible
class AdditionalFieldValue(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='additional_values')
    field = models.ForeignKey(AdditionalField, on_delete=models.CASCADE, related_name='+')
    value = models.CharField(max_length=256)

    class Meta:
        ordering = ('user', 'field')

        verbose_name = _('Additional field value')
        verbose_name_plural = _('Additional field values')

    def __str__(self):
        return self.user.username + '/' + self.field.key
