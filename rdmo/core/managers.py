from functools import reduce

from django.core.exceptions import FieldDoesNotExist
from django.conf import settings
from django.db import models

from rdmo.management.rules import is_an_editor, is_multisite_editor, \
                                    is_a_reviewer, is_multisite_reviewer

from .constants import PERMISSIONS

class CurrentSiteQuerySetMixin(object):
    
    def filter_current_site(self):
        return self.filter(models.Q(sites=None) | models.Q(sites=settings.SITE_ID))

class EditableElementQuerySetMixin(models.QuerySet):

    def filter_related_to_user_role(self, user):
        ''' returns all objects that are related to the user editor or reviewer role'''


        related_Q = None

        try:
            get_field = self.model._meta.get_field('sites')
            sites_Q = (
                models.Q(sites__in=user.role.editor.all()) |
                models.Q(sites__in=user.role.reviewer.all())
                )
            related_Q = sites_Q
        except FieldDoesNotExist:
            pass

        try:
            get_field = self.model._meta.get_field('editors')
            editors_Q = (
                models.Q(editors=None) |
                models.Q(editors__in=user.role.editor.all()) |
                models.Q(editors__in=user.role.reviewer.all())
            )

            related_Q = related_Q | editors_Q if related_Q is not None else editors_Q

        except FieldDoesNotExist:
            pass
        # breakpoint()
        return related_Q

    def filter_user(self, user):
        if not user.is_authenticated:
            return self.none()

        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label

        if not user.has_perm('%s.view_%s' % (app_label, model_name)):
            return self.none()

        if is_multisite_editor(user) or is_multisite_reviewer(user) or \
                user.is_superuser:
            return self.all()
        elif is_an_editor(user) or is_a_reviewer(user):
            related_Q = self.filter_related_to_user_role(user)
            return self.filter(related_Q) if related_Q is not None else self.none()
        else:
            return self.none()


class GroupsQuerySetMixin(object):

    def filter_group(self, user):
        groups = user.groups.all()
        return self.filter(models.Q(groups=None) | models.Q(groups__in=groups))


class AvailabilityQuerySetMixin(object):

    def filter_availability(self, user):
        model = str(self.model._meta)
        permissions = PERMISSIONS[model]

        if user.has_perms(permissions):
            return self
        else:
            return self.filter(available=True)


class CurrentSiteManagerMixin(object):

    def filter_current_site(self):
        return self.get_queryset().filter_current_site()


class EditableElementManagerMixin(object):

    def filter_user(self, user):
        return self.get_queryset().filter_user(user)


class GroupsManagerMixin(object):

    def filter_group(self, user):
        return self.get_queryset().filter_group(user)


class AvailabilityManagerMixin(object):

    def filter_availability(self, user):
        return self.get_queryset().filter_availability(user)
