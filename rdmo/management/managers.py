
from django.db.models import QuerySet

from rdmo.core.managers import (
    AvailabilityQuerySetMixin,
    ForCatalogQuerySetMixin,
    ForGroupsQuerySetMixin,
    ForSiteQuerySetMixin,
)


class ForProjectQuerySet(ForSiteQuerySetMixin, ForGroupsQuerySetMixin, ForCatalogQuerySetMixin,
                         AvailabilityQuerySetMixin, QuerySet):

    def filter_for_project(self, project, user=None):
        qs = (
            self.filter_for_site(project.site)
            .filter_for_catalog(project.catalog)
            .filter_for_groups(project.groups)
        )
        if user is not None:
            return qs.filter_availability(user)
        else:
            return qs.filter(available=True)

class ForProjectManagerMixin:

    def get_queryset(self):
        return ForProjectQuerySet(self.model, using=self._db)

    def filter_for_project(self, project, user=None):
        return self.get_queryset().filter_for_project(project, user=user)
