from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy

from rdmo.core.models import Model


class Visibility(Model):

    project = models.OneToOneField(
        'Project', on_delete=models.CASCADE,
        verbose_name=_('Project'),
        help_text=_('The project for this visibility.')
    )
    sites = models.ManyToManyField(
        Site, blank=True,
        verbose_name=_('Sites'),
        help_text=_('The sites for which the project is visible (in a multi site setup).')
    )
    groups = models.ManyToManyField(
        Group, blank=True,
        verbose_name=_('Group'),
        help_text=_('The groups for which the project is visible.')
    )

    class Meta:
        ordering = ('project', )
        verbose_name = _('Visibility')
        verbose_name_plural = _('Visibilities')

    def __str__(self):
        return str(self.project)

    def is_visible(self, user):
        return (
            not self.sites.exists() or self.sites.filter(id=settings.SITE_ID).exists()
        ) and (
            not self.groups.exists() or self.groups.filter(id__in=[group.id for group in user.groups.all()]).exists()
        )

    def get_help_display(self):
        sites = self.sites.values_list('domain', flat=True)
        groups = self.groups.values_list('name', flat=True)

        if sites and groups:
            return ngettext_lazy(
                'This project can be accessed by all users on %s or in the group %s.',
                'This project can be accessed by all users on %s or in the groups %s.',
                len(groups)
            ) % (
                ', '.join(sites),
                ', '.join(groups)
            )
        elif sites:
            return _('This project can be accessed by all users on %s.') % ', '.join(sites)
        elif groups:
            return ngettext_lazy(
                'This project can be accessed by all users in the group %s.',
                'This project can be accessed by all users in the groups %s.',
                len(groups)
            ) % ', '.join(groups)
        else:
            return _('This project can be accessed by all users.')
