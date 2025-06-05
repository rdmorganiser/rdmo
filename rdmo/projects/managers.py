from django.conf import settings
from django.db import models
from django.db.models import Q

from mptt.models import TreeManager
from mptt.querysets import TreeQuerySet

from rdmo.accounts.utils import is_site_manager
from rdmo.core.managers import CurrentSiteManagerMixin


class ProjectQuerySet(TreeQuerySet):

    def filter_user(self, user, filter_for_user=False):
        if user.is_authenticated:
            if user.has_perm('projects.view_project') and not filter_for_user:
                # return all projects for admins or users with model permissions (unless filter_for_user is set)
                return self.all()
            else:
                # create a filter for all project where this user is a member
                user_filter = Q(user=user)

                # create a filter for all projects which are visible for this user
                groups = user.groups.all()
                sites_filter = Q(visibility__sites=None) | Q(visibility__sites=settings.SITE_ID)
                groups_filter = Q(visibility__groups=None) | Q(visibility__groups__in=groups)
                visibility_filter = Q(visibility__isnull=False) & sites_filter & groups_filter

                # create a filter for all projects of this site (unless filter_for_user is set)
                if (user.has_perm('projects.view_project') or is_site_manager(user)) and not filter_for_user:
                    current_site_filter = Q(site=settings.SITE_ID)
                else:
                    current_site_filter = Q()

                # create queryset by combining all three filters
                queryset = self.filter(user_filter | visibility_filter | current_site_filter)

                # add descendant projects
                for instance in queryset:
                    queryset |= instance.get_descendants()
                return queryset.distinct()
        else:
            return self.none()

    def filter_catalogs(self, catalogs=None, exclude_catalogs=None, exclude_null=True):
        catalogs_filter = Q()
        if exclude_null:
          catalogs_filter &= Q(catalog__isnull=False)
        if catalogs:
            catalogs_filter &= Q(catalog__in=catalogs)
        if exclude_catalogs:
            catalogs_filter &= ~Q(catalog__in=exclude_catalogs)
        return self.filter(catalogs_filter)

    def filter_groups(self, groups):
        if not groups:
            return self

        # need to import here to prevent circular import
        # queryset methods need to be refactored in modules otherwise
        from django.contrib.auth import get_user_model

        from rdmo.projects.models import Membership

        # users in the given groups
        users = get_user_model().objects.filter(groups__in=groups)
        # memberships for those users with role 'owner'
        memberships = Membership.objects.filter(role='owner', user__in=users)
        # projects that have those memberships
        return self.filter(memberships__in=memberships).distinct()

    def filter_projects_for_task_or_view(self, instance):

        # if View/Task is not available it should not show for any project
        if not instance.available:
            return self.none()

        # projects that have an unavailable catalog should be disregarded
        qs = self.filter(catalog__available=True)

        # when instance.catalogs is empty it applies to all
        if instance.catalogs.exists():
            qs = qs.filter(catalog__in=instance.catalogs.all())

        # when instance.sites is empty it applies to all
        if instance.sites.exists():
            qs = qs.filter(site__in=instance.sites.all())

        # when instance.groups is empty it applies to all
        if instance.groups.exists():
            qs = qs.filter_groups(instance.groups.all())

        return qs


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

    def filter_empty(self):
        return self.filter((Q(text='') | Q(text=None)) & Q(option=None) & (Q(file='') | Q(file=None)))

    def exclude_empty(self):
        return self.exclude((Q(text='') | Q(text=None)) & Q(option=None) & (Q(file='') | Q(file=None)))

    def distinct_list(self):
        return self.order_by('attribute').values_list('attribute', 'set_prefix', 'set_index').distinct()

    def filter_set(self, set_value):
        # get the catalog and prefetch most elements of the catalog
        catalog = set_value.project.catalog
        catalog.prefetch_elements()

        # Get all attributes from matching elements and their descendants
        attributes = {
            descendant.attribute
            for element in (catalog.pages + catalog.questions)
            if element.attribute == set_value.attribute
            for descendant in element.descendants
        }

        # construct the set_prefix for descendants for this set
        descendants_set_prefix = \
            f'{set_value.set_prefix}|{set_value.set_index}' if set_value.set_prefix else str(set_value.set_index)

        # collect all values for this set and all descendants
        return self.filter(project=set_value.project, snapshot=set_value.snapshot, attribute__in=attributes).filter(
            Q(set_prefix=set_value.set_prefix, set_index=set_value.set_index) |
            Q(set_prefix__startswith=descendants_set_prefix)
        )


class ProjectManager(CurrentSiteManagerMixin, TreeManager):

    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self._db)

    def filter_user(self, user, filter_for_user=False):
        return self.get_queryset().filter_user(user, filter_for_user)

    def filter_catalogs(self, catalogs=None, exclude_catalogs=None, exclude_null=True):
        return self.get_queryset().filter_catalogs(catalogs=catalogs, exclude_catalogs=exclude_catalogs,
                                                   exclude_null=exclude_null)
    def filter_groups(self, groups):
        return self.get_queryset().filter_groups(groups)

    def filter_projects_for_task_or_view(self, instance):
        return self.get_queryset().filter_projects_for_task_or_view(instance)


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
