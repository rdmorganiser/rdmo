from django.conf import settings
from django.db import models

from mptt.models import TreeManager
from mptt.querysets import TreeQuerySet

from rdmo.accounts.utils import is_site_manager
from rdmo.core.managers import CurrentSiteManagerMixin


class ProjectQuerySet(TreeQuerySet):

    def filter_current_site(self):
        return self.filter(site=settings.SITE_ID)

    def filter_user(self, user):
        if user.is_authenticated:
            if user.has_perm('projects.view_project'):
                return self.all()
            elif is_site_manager(user):
                return self.filter_current_site()
            else:
                queryset = self.filter(user=user)
                for instance in queryset:
                    queryset |= instance.get_descendants()
                return queryset.distinct()
        else:
            return self.none()


class MembershipQuerySet(models.QuerySet):

    def filter_current_site(self):
        return self.filter(project__site=settings.SITE_ID)

    def filter_user(self, user):
        if user.is_authenticated:
            if user.has_perm('projects.view_membership'):
                return self.all()
            elif is_site_manager(user):
                return self.filter_current_site()
            else:
                from .models import Project
                projects = Project.objects.filter_user(user)
                return self.filter(project__in=projects)
        else:
            return self.objects.none()


class IssueQuerySet(models.QuerySet):

    def filter_current_site(self):
        return self.filter(project__site=settings.SITE_ID)

    def filter_user(self, user):
        if user.is_authenticated:
            if user.has_perm('projects.view_integration'):
                return self.all()
            elif is_site_manager(user):
                return self.filter_current_site()
            else:
                from .models import Project
                projects = Project.objects.filter_user(user)
                return self.filter(project__in=projects)
        else:
            return self.none()


class IntegrationQuerySet(models.QuerySet):

    def filter_current_site(self):
        return self.filter(project__site=settings.SITE_ID)

    def filter_user(self, user):
        if user.is_authenticated:
            if user.has_perm('projects.view_issue'):
                return self.all()
            elif is_site_manager(user):
                return self.filter_current_site()
            else:
                from .models import Project
                projects = Project.objects.filter_user(user)
                return self.filter(project__in=projects)
        else:
            return self.none()


class InviteQuerySet(models.QuerySet):

    def filter_current_site(self):
        return self.filter(project__site=settings.SITE_ID)

    def filter_user(self, user):
        if user.is_authenticated:
            if user.has_perm('projects.view_invite'):
                return self.all()
            elif is_site_manager(user):
                return self.filter_current_site()
            else:
                from .models import Project
                projects = Project.objects.filter(memberships__user=user, memberships__role='owner')
                return self.filter(project__in=projects)
        else:
            return self.none()


class SnapshotQuerySet(models.QuerySet):

    def filter_current_site(self):
        return self.filter(project__site=settings.SITE_ID)

    def filter_user(self, user):
        if user.is_authenticated:
            if user.has_perm('projects.view_snapshot'):
                return self.all()
            elif is_site_manager(user):
                return self.filter_current_site()
            else:
                from .models import Project
                projects = Project.objects.filter_user(user)
                return self.filter(project__in=projects)
        else:
            return self.none()


class ValueQuerySet(models.QuerySet):

    def filter_current_site(self):
        return self.filter(project__site=settings.SITE_ID)

    def filter_user(self, user):
        if user.is_authenticated:
            if user.has_perm('projects.view_value'):
                return self.all()
            elif is_site_manager(user):
                return self.filter_current_site()
            else:
                from .models import Project
                projects = Project.objects.filter_user(user)
                return self.filter(project__in=projects)
        else:
            return self.none()


class ProjectManager(CurrentSiteManagerMixin, TreeManager):

    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self._db)

    def filter_user(self, user):
        return self.get_queryset().filter_user(user)


class MembershipManager(CurrentSiteManagerMixin, models.Manager):

    def get_queryset(self):
        return MembershipQuerySet(self.model, using=self._db)

    def filter_user(self, user):
        return self.get_queryset().filter_user(user)


class IssueManager(CurrentSiteManagerMixin, models.Manager):

    def get_queryset(self):
        return IssueQuerySet(self.model, using=self._db)

    def filter_user(self, user):
        return self.get_queryset().filter_user(user)

    def active(self):
        return self.get_queryset().active()


class IntegrationManager(CurrentSiteManagerMixin, models.Manager):

    def get_queryset(self):
        return IntegrationQuerySet(self.model, using=self._db)

    def filter_user(self, user):
        return self.get_queryset().filter_user(user)


class InviteManager(CurrentSiteManagerMixin, models.Manager):

    def get_queryset(self):
        return InviteQuerySet(self.model, using=self._db)

    def filter_user(self, user):
        return self.get_queryset().filter_user(user)


class SnapshotManager(CurrentSiteManagerMixin, models.Manager):

    def get_queryset(self):
        return SnapshotQuerySet(self.model, using=self._db)

    def filter_user(self, user):
        return self.get_queryset().filter_user(user)


class ValueManager(CurrentSiteManagerMixin, models.Manager):

    def get_queryset(self):
        return ValueQuerySet(self.model, using=self._db)

    def filter_user(self, user):
        return self.get_queryset().filter_user(user)
