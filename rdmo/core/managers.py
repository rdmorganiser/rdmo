from django.conf import settings
from django.db import models

from .utils import can_view_unavailable


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
        if can_view_unavailable(user, self.model):
            return self
        else:
            return self.filter(available=True)


class CurrentSiteManagerMixin:

    def filter_current_site(self):
        return self.get_queryset().filter_current_site()


class GroupsManagerMixin:

    def filter_group(self, user):
        return self.get_queryset().filter_group(user)


class AvailabilityManagerMixin:

    def filter_availability(self, user):
        return self.get_queryset().filter_availability(user)
