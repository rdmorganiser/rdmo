from django.db import models

from rdmo.core.managers import (
    AvailabilityManagerMixin,
    AvailabilityQuerySetMixin,
    CurrentSiteManagerMixin,
    CurrentSiteQuerySetMixin,
    ForCatalogQuerySetMixin,
    ForGroupQuerySetMixin,
    ForSiteQuerySetMixin,
    GroupsManagerMixin,
    GroupsQuerySetMixin,
)


class PluginQuerySet(
    ForSiteQuerySetMixin, ForGroupQuerySetMixin, ForCatalogQuerySetMixin,
    CurrentSiteQuerySetMixin, GroupsQuerySetMixin, AvailabilityQuerySetMixin,
    models.QuerySet):

    def filter_for_project(self, project):
        return (
            self
                .filter(available=True)
                .filter_for_site(project.site)
                .filter_for_catalog(project.catalog)
                .filter_for_groups(project.groups)
        )
    def filter_current_available(self, user):
        return (
            self
            .filter_current_site()
            .filter_availability(user)
        )

class PluginManager(CurrentSiteManagerMixin, GroupsManagerMixin, AvailabilityManagerMixin, models.Manager):

    def get_queryset(self) -> PluginQuerySet:
        return PluginQuerySet(self.model, using=self._db)

    def filter_current_site(self):
        return self.get_queryset().filter_current_site()

    def filter_for_project(self, project):
        return self.get_queryset().filter_for_project(project)

    def filter_current_available(self, user):
        return self.get_queryset().filter_current_available(user)
