from django.conf import settings
from django.db import models

from rdmo.core.managers import (
    AvailabilityManagerMixin,
    AvailabilityQuerySetMixin,
    CurrentSiteManagerMixin,
    CurrentSiteQuerySetMixin,
    ForSiteQuerySetMixin,
    GroupsManagerMixin,
    GroupsQuerySetMixin,
)


class PluginQuerySet(ForSiteQuerySetMixin, CurrentSiteQuerySetMixin, GroupsQuerySetMixin,
                     AvailabilityQuerySetMixin, models.QuerySet):

    def filter_for_project(self, project):
        return (
            self
                .filter_for_site(project.site)
                .filter(models.Q(catalogs=None) | models.Q(catalogs=project.catalog))
                .filter(models.Q(groups=None) | models.Q(groups__in=project.groups))
        )

    def filter_for_settings(self):
        if not settings.PLUGINS:
            return self.none()

        return self.filter(python_path__in=settings.PLUGINS)

    def filter_for_plugin_type(self, plugin_type=None, plugin_types=None):
        if plugin_type is not None and plugin_types is not None:
            raise ValueError('Pass either plugin_type or plugin_types, not both.')

        if plugin_type is not None:
            return self.filter(plugin_type=plugin_type)

        if plugin_types is not None:
            return self.filter(plugin_type__in=plugin_types)

        return self


    def for_context(self, project=None, plugin_type=None, plugin_types=None,
                    user=None, url_name=None):
        queryset = self

        # filter by settings.PLUGINS
        queryset = queryset.filter_for_settings()

        # filter by project .site,.catalog and .groups
        if project is not None:
            queryset = queryset.filter_for_project(project)

        # filter by availability
        if user is not None:
            queryset = queryset.filter_availability(user)
        else:
            queryset = queryset.filter(available=True)

        # filter by current site
        queryset = queryset.filter_current_site()

        # filter by optional plugin type(s)
        queryset = queryset.filter_for_plugin_type(plugin_type=plugin_type, plugin_types=plugin_types)

        # filter by optional url_name
        if url_name is not None:
            queryset = queryset.filter(url_name=url_name)

        return queryset


class PluginManager(CurrentSiteManagerMixin, GroupsManagerMixin, AvailabilityManagerMixin, models.Manager):

    def get_queryset(self) -> PluginQuerySet:
        return PluginQuerySet(self.model, using=self._db)

    def filter_current_site(self):
        return self.get_queryset().filter_current_site()

    def filter_for_project(self, project):
        return self.get_queryset().filter_for_project(project)

    def filter_for_settings(self):
        return self.get_queryset().filter_for_settings()

    def for_context(self, project=None, plugin_type=None, plugin_types=None,
                    user=None, url_name=None):
        return self.get_queryset().for_context(
            project=project,
            plugin_type=plugin_type,
            plugin_types=plugin_types,
            user=user,
            url_name=url_name
        )
