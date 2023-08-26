from django.db import models

from rdmo.core.managers import (
    AvailabilityManagerMixin,
    AvailabilityQuerySetMixin,
    CurrentSiteManagerMixin,
    CurrentSiteQuerySetMixin,
    GroupsManagerMixin,
    GroupsQuerySetMixin,
)


class ViewQuestionSet(CurrentSiteQuerySetMixin, GroupsQuerySetMixin, AvailabilityQuerySetMixin, models.QuerySet):

    def filter_catalog(self, catalog):
        return self.filter(models.Q(catalogs=None) | models.Q(catalogs=catalog))


class ViewManager(CurrentSiteManagerMixin, GroupsManagerMixin, AvailabilityManagerMixin, models.Manager):

    def get_queryset(self):
        return ViewQuestionSet(self.model, using=self._db)

    def filter_catalog(self, catalog):
        return self.get_queryset().filter_catalog(catalog)
