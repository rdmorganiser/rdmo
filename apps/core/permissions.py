from django.core.exceptions import ImproperlyConfigured

from rest_framework.permissions import BasePermission


class HasRulesPermission(BasePermission):

    perms_map = {
        'GET': 'view',
        'OPTIONS': 'view',
        'HEAD': 'view',
        'POST': 'add',
        'PUT': 'update',
        'PATCH': 'update',
        'DELETE': 'delete'
    }

    def get_permission_required(self, view, method):
        '''
        inspired by django.contrib.auth.mixins.PermissionRequiredMixin
        '''
        if view.permission_required is None:
            raise ImproperlyConfigured('%s is missing the permission_required attribute.' % view.__class__.__name__)

        permission_required = view.permission_required[self.perms_map[method]]

        if isinstance(permission_required, str):
            perms = (permission_required, )
        else:
            perms = permission_required
        return perms

    def has_permission(self, request, view):
        try:
            obj = view.get_permission_object()
        except AttributeError:
            obj = None

        perms = self.get_permission_required(view, request.method)

        if obj:
            return request.user.has_perms(perms, obj)
        else:
            return request.user.has_perms(perms)

    def has_object_permission(self, request, view, obj):
        try:
            obj = view.get_permission_object()
        except AttributeError:
            pass

        perms = self.get_permission_required(view, request.method)
        return request.user.has_perms(perms, obj)
