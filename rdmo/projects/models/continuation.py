from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from rdmo.core.models import Model
from rdmo.questions.models import Page


class Continuation(Model):

    project = models.ForeignKey(
        'Project', on_delete=models.CASCADE, related_name='+',
        verbose_name=_('Project'),
        help_text=_('The project for this continuation.')
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+',
        verbose_name=_('User'),
        help_text=_('The user for this continuation.')
    )
    page = models.ForeignKey(
        Page, null=True, on_delete=models.CASCADE, related_name='+',
        verbose_name=_('Page'),
        help_text=_('The page for this continuation.')
    )

    class Meta:
        ordering = ('user', 'project')
        verbose_name = _('Continuation')
        verbose_name_plural = _('Continuations')

    def __str__(self):
        return f'{self.project}/{self.user}/{self.page}'
