from django.db.models import Manager, QuerySet

from rdmo.core.managers import (
    AvailabilityManagerMixin,
    AvailabilityQuerySetMixin,
    CurrentSiteManagerMixin,
    ForCatalogQuerySetMixin,
    ForGroupsQuerySetMixin,
    ForSiteQuerySetMixin,
    GroupsManagerMixin,
)


class TaskQuerySet(ForSiteQuerySetMixin, ForGroupsQuerySetMixin, ForCatalogQuerySetMixin,
                   AvailabilityQuerySetMixin, QuerySet):

    def filter_for_project(self, project):
        return (
            self.filter(available=True)
                .filter_for_site(project.site)
                .filter_for_catalog(project.catalog)
                .filter_for_groups(project.groups)
        )

class TaskManager(CurrentSiteManagerMixin, GroupsManagerMixin, AvailabilityManagerMixin, Manager):

    def get_queryset(self) -> TaskQuerySet:
        return TaskQuerySet(self.model, using=self._db)

    def filter_for_project(self, project):
        return self.get_queryset().filter_for_project(project)
