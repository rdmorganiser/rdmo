from django.conf import settings
from django.db import connections, models

from rdmo.core.managers import (
    AvailabilityManagerMixin,
    AvailabilityQuerySetMixin,
    CurrentSiteManagerMixin,
    CurrentSiteQuerySetMixin,
    ForSiteQuerySetMixin,
    GroupsManagerMixin,
    GroupsQuerySetMixin,
)


class PluginQuerySet(
    ForSiteQuerySetMixin,
    CurrentSiteQuerySetMixin, GroupsQuerySetMixin, AvailabilityQuerySetMixin,
    models.QuerySet):

    def filter_for_project(self, project):
        return (
            self
                .filter_for_site(project.site)
                .filter(catalogs=project.catalog)
                .filter(models.Q(groups=None) | models.Q(groups__in=project.groups))
        )

    def filter_for_settings_plugins(self):
        if not settings.PLUGINS:
            return self

        return self.filter(python_path__in=settings.PLUGINS)

    def filter_for_format(self, file_format: str):
        if not file_format:
            return self

        qs = (
            models.Q(url_name=file_format)
            | models.Q(uri_path=file_format)
            | models.Q(uri_path__endswith=f'/{file_format}')
        )

        # add a JSONField contains lookup if the current DB supports it
        connection = connections[self.db]
        if getattr(connection.features, 'supports_json_field_contains', False):
            qs |= models.Q(plugin_settings__contains={'format': file_format})
        elif connection.vendor == 'sqlite':
            # SQLite: JSONField is stored as TEXT; emulate contains by string search.
            qs |= models.Q(plugin_settings__icontains=f'"format": "{file_format}"')

        return self.filter(qs)


    def for_context(self, project=None, plugin_type=None, plugin_types=None,
                    user=None, format=None):
        qs = self

        # filter by settings.PLUGINS
        qs = qs.filter_for_settings_plugins()

        # filter by project .site,.catalog and .groups
        if project is not None:
            qs = qs.filter_for_project(project)

        # filter by availability
        if user is not None:
            qs = qs.filter_availability(user)
        else:
            qs = qs.filter(available=True)

        # filter by current site
        qs = qs.filter_current_site()

        # filter by optional plugin type(s)
        if plugin_type is not None and plugin_types is not None:
            raise ValueError('Pass either plugin_type or plugin_types, not both.')

        if plugin_type is not None:
            qs = qs.filter(plugin_type=plugin_type)
        elif plugin_types is not None:
            qs = qs.filter(plugin_type__in=plugin_types)

        # filter by optional format
        if format is not None:
            qs = qs.filter_for_format(format)

        return qs

class PluginManager(CurrentSiteManagerMixin, GroupsManagerMixin, AvailabilityManagerMixin, models.Manager):

    def get_queryset(self) -> PluginQuerySet:
        return PluginQuerySet(self.model, using=self._db)

    def filter_current_site(self):
        return self.get_queryset().filter_current_site()

    def filter_for_project(self, project):
        return self.get_queryset().filter_for_project(project)

    def filter_for_settings_plugins(self):
        return self.get_queryset().filter_for_settings_plugins()

    def filter_for_format(self, file_format):
        return self.get_queryset().filter_for_format(file_format)

    def for_context(self, project=None, plugin_type=None, plugin_types=None,
                    user=None, format=None):
        return self.get_queryset().for_context(
            project=project,
            plugin_type=plugin_type,
            plugin_types=plugin_types,
            user=user,
            format=format
        )
