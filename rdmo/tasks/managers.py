from django.db import models

from rdmo.core.managers import (
    AvailabilityManagerMixin,
    AvailabilityQuerySetMixin,
    CurrentSiteManagerMixin,
    CurrentSiteQuerySetMixin,
    GroupsManagerMixin,
    GroupsQuerySetMixin,
)


class TaskQuestionSet(CurrentSiteQuerySetMixin, GroupsQuerySetMixin, AvailabilityQuerySetMixin, models.QuerySet):

    def filter_catalog(self, catalog):
        return self.filter(models.Q(catalogs=None) | models.Q(catalogs=catalog))

    def filter_available_views_for_project(self, project):
        return (self
            .filter(sites=project.site)
            .filter(catalogs=project.catalog)
            .filter_group(project.owners)
            .filter(available=True)
            .exclude(catalogs=None)
        )



class TaskManager(CurrentSiteManagerMixin, GroupsManagerMixin, AvailabilityManagerMixin, models.Manager):

    def get_queryset(self):
        return TaskQuestionSet(self.model, using=self._db)

    def filter_catalog(self, catalog):
        return self.get_queryset().filter_catalog(catalog)

    def filter_available_tasks_for_project(self, project):
        return self.get_queryset().filter_available_views_for_project(project)
