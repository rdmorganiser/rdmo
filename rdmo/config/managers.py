from django.db import models
from django.db.models import Q

from rdmo.core.managers import (
    AvailabilityManagerMixin,
    AvailabilityQuerySetMixin,
    CurrentSiteManagerMixin,
    CurrentSiteQuerySetMixin,
    GroupsManagerMixin,
    GroupsQuerySetMixin,
)


class PluginQuerySet(CurrentSiteQuerySetMixin, GroupsQuerySetMixin, AvailabilityQuerySetMixin, models.QuerySet):

    def filter_catalog(self, catalog):
        return self.filter(models.Q(catalogs=None) | models.Q(catalogs=catalog))

    def filter_for_site(self, site):
        return self.filter(Q(sites=None) | Q(sites=site))

    def filter_for_group(self, groups):
        return self.filter(Q(groups=None) | Q(groups__in=groups))

    def filter_for_project(self, project):
        return (
            self
                .filter(available=True)
                .filter_for_site(project.site)
                .filter_catalog(project.catalog)
                .filter_for_group(project.groups)
        )

class PluginManager(CurrentSiteManagerMixin, GroupsManagerMixin, AvailabilityManagerMixin, models.Manager):

    def get_queryset(self) -> PluginQuerySet:
        return PluginQuerySet(self.model, using=self._db)

    def filter_catalog(self, catalog):
        return self.get_queryset().filter_catalog(catalog)

    def filter_for_project(self, project):
        return self.get_queryset().filter_for_project(project)
