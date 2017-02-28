from django.core.exceptions import ImproperlyConfigured

from rest_framework.permissions import BasePermission, DjangoModelPermissions


class HasModelPermission(DjangoModelPermissions):

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class HasObjectPermission(BasePermission):

    perms_map = {
        'GET': 'view',
        'OPTIONS': 'view',
        'HEAD': 'view',
        'POST': 'add',
        'PUT': 'change',
        'PATCH': 'change',
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
