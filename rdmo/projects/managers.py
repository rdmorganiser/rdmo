from django.conf import settings
from django.db import models

from rdmo.core.managers import CurrentSiteManagerMixin


class ProjectQuerySet(models.QuerySet):

    def filter_current_site(self):
        return self.filter(site=settings.SITE_ID)


class MembershipQuerySet(models.QuerySet):

    def filter_current_site(self):
        return self.filter(project__site=settings.SITE_ID)


class SnapshotQuerySet(models.QuerySet):

    def filter_current_site(self):
        return self.filter(project__site=settings.SITE_ID)


class ValueQuerySet(models.QuerySet):

    def filter_current_site(self):
        return self.filter(project__site=settings.SITE_ID)


class ProjectManager(CurrentSiteManagerMixin, models.Manager):

    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self._db)


class MembershipManager(CurrentSiteManagerMixin, models.Manager):

    def get_queryset(self):
        return MembershipQuerySet(self.model, using=self._db)


class SnapshotManager(CurrentSiteManagerMixin, models.Manager):

    def get_queryset(self):
        return SnapshotQuerySet(self.model, using=self._db)


class ValueManager(CurrentSiteManagerMixin, models.Manager):

    def get_queryset(self):
        return ValueQuerySet(self.model, using=self._db)
