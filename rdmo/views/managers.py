from django.contrib.sites.managers import CurrentSiteManager
from django.db.models import Q


class ViewManager(CurrentSiteManager):

    def active(self, user):
        groups = user.groups.all()
        return super().get_queryset().filter(Q(groups=None) | Q(groups__in=groups))
