from django.conf import settings
from django.db import models


class CurrentSiteQuerySetMixin(object):

    def filter_current_site(self):
        return self.filter(sites=settings.SITE_ID)


class GroupsQuerySetMixin(object):

    def filter_group(self, user):
        groups = user.groups.all()
        return self.filter(models.Q(groups=None) | models.Q(groups__in=groups))


class CurrentSiteManagerMixin(object):

    def filter_current_site(self):
        return self.get_queryset().filter_current_site()


class GroupsManagerMixin(object):

    def filter_group(self, user):
        return self.get_queryset().filter_group(user)
