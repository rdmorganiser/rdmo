from django.db.models import Manager, Q, QuerySet

from rdmo.core.managers import (
    AvailabilityManagerMixin,
    AvailabilityQuerySetMixin,
    CurrentSiteManagerMixin,
    CurrentSiteQuerySetMixin,
    GroupsManagerMixin,
    GroupsQuerySetMixin,
)


class TaskQuestionSet(CurrentSiteQuerySetMixin, GroupsQuerySetMixin, AvailabilityQuerySetMixin, QuerySet):

    def filter_catalog(self, catalog):
        return self.filter(Q(catalogs=None) | Q(catalogs=catalog))

    def filter_available_tasks_for_project(self, project):
        site_filter = Q(sites=project.site) | Q(sites__isnull=True)
        catalogs_filter = Q(catalogs=project.catalog) | Q(catalogs__isnull=True)
        groups_filter = Q(groups__in=project.groups) | Q(groups__isnull=True)
        availability_filter = Q(available=True)

        return self.filter(site_filter & catalogs_filter & groups_filter & availability_filter)



class TaskManager(CurrentSiteManagerMixin, GroupsManagerMixin, AvailabilityManagerMixin, Manager):

    def get_queryset(self) -> TaskQuestionSet:
        return TaskQuestionSet(self.model, using=self._db)

    def filter_catalog(self, catalog):
        return self.get_queryset().filter_catalog(catalog)

    def filter_available_tasks_for_project(self, project):
        return self.get_queryset().filter_available_tasks_for_project(project)
