from django.conf import settings
from django.db import models
from django.db.models import Q

from .constants import PERMISSIONS


class CurrentSiteQuerySetMixin:

    def filter_current_site(self):
        if settings.MULTISITE:
            return self.filter(sites=settings.SITE_ID)
        else:
            return self.filter(models.Q(sites=None) | models.Q(sites=settings.SITE_ID))


class GroupsQuerySetMixin:

    def filter_group(self, user):
        groups = user.groups.all()
        return self.filter(models.Q(groups=None) | models.Q(groups__in=groups))


class AvailabilityQuerySetMixin:

    def filter_availability(self, user):
        if user.has_perms(PERMISSIONS[self.model._meta.label_lower]):
            return self
        else:
            return self.filter(available=True)


class ForGroupsQuerySetMixin:

    def filter_for_groups(self, groups):
        return self.filter(Q(groups=None) | Q(groups__in=groups))


class ForSiteQuerySetMixin:

    def filter_for_site(self, site):
        if settings.MULTISITE:
            return self.filter(sites=site)
        else:
            return self.filter(Q(sites=None) | Q(sites=site))


class ForCatalogQuerySetMixin:

    def filter_for_catalog(self, catalog):
        return self.filter(models.Q(catalogs=None) | models.Q(catalogs=catalog))


class CurrentSiteManagerMixin:

    def filter_current_site(self):
        return self.get_queryset().filter_current_site()


class GroupsManagerMixin:

    def filter_group(self, user):
        return self.get_queryset().filter_group(user)


class AvailabilityManagerMixin:

    def filter_availability(self, user):
        return self.get_queryset().filter_availability(user)
