from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from rdmo.services.utils import get_provider

from ..managers import IntegrationManager


class Integration(models.Model):

    objects = IntegrationManager()

    project = models.ForeignKey(
        'Project', on_delete=models.CASCADE, related_name='integrations',
        verbose_name=_('Project'),
        help_text=_('The project for this integration.')
    )
    provider_key = models.TextField(
        verbose_name=_('Provider key'),
        help_text=_('The key of the provider for this integration.')
    )

    class Meta:
        ordering = ('project__title', )
        verbose_name = _('Integration')
        verbose_name_plural = _('Integrations')

    def __str__(self):
        return '%s / %s' % (self.project.title, self.provider_key)

    @property
    def provider(self):
        return get_provider(self.provider_key)

    @property
    def options_dict(self):
        return dict(self.options.values_list('key', 'value'))

    def get_absolute_url(self):
        return reverse('project', kwargs={'pk': self.project.pk})


class IntegrationOption(models.Model):

    integration = models.ForeignKey(
        'Integration', on_delete=models.CASCADE, related_name='options',
        verbose_name=_('Integration'),
        help_text=_('The integration for this integration option.')
    )
    key = models.SlugField(
        max_length=128,
        verbose_name=_('Key'),
        help_text=_('The key for this integration option.')
    )
    value = models.TextField(
        verbose_name=_('Value'),
        help_text=_('The value for this integration option.')
    )

    class Meta:
        ordering = ('integration__project__title', )
        verbose_name = _('Integration option')
        verbose_name_plural = _('Integration options')

    def __str__(self):
        return '%s / %s / %s = %s' % (self.integration.project.title, self.integration.provider_key, self.key, self.value)
