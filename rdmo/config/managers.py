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

    def for_context(self, project=None, plugin_type=None, user=None):
        qs = self

        if project is not None:
            qs = qs.filter_for_project(project)

        if user is not None:
            qs = qs.filter_current_available(user)
        else:
            qs = qs.filter(available=True).filter_current_site()

        if plugin_type is not None:
            qs = qs.filter(plugin_type=plugin_type)

        return qs

class PluginManager(CurrentSiteManagerMixin, GroupsManagerMixin, AvailabilityManagerMixin, models.Manager):

    def get_queryset(self) -> PluginQuerySet:
        return PluginQuerySet(self.model, using=self._db)

    def filter_current_site(self):
        return self.get_queryset().filter_current_site()

    def filter_for_project(self, project):
        return self.get_queryset().filter_for_project(project)

    def filter_current_available(self, user):
        return self.get_queryset().filter_current_available(user)

    def for_context(self, project=None, plugin_type=None, user=None):
        return self.get_queryset().for_context(
            project=project,
            plugin_type=plugin_type,
            user=user,
        )
