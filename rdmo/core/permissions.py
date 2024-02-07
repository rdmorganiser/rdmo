import logging

from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions

logger = logging.getLogger(__name__)


def log_result(func):
    '''
    A decorator to automatically log the arguments and the results of calls
    to has_permission and has_object_permission.
    '''
    def wrapper(self, request, *args):
        result = func(self, request, *args)

        class_name = self.__class__.__name__
        func_name = func.__name__
        logger.debug('%s.%s path=%s method=%s user=%s result=%s',
                     class_name, func_name, request.path, request.method, request.user, result)
        return result

    return wrapper


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

    @log_result
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        return super().has_permission(request, view)

    @log_result
    def has_object_permission(self, request, view, obj):
        if not (request.user and request.user.is_authenticated):
            return False

        # has_object_permission needs to follow has_permission
        return self.has_permission(request, view)


class HasObjectPermission(DjangoObjectPermissions):

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s_object'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s_object'],
        'HEAD': ['%(app_label)s.view_%(model_name)s_object'],
        'POST': ['%(app_label)s.add_%(model_name)s_object'],
        'PUT': ['%(app_label)s.change_%(model_name)s_object'],
        'PATCH': ['%(app_label)s.change_%(model_name)s_object'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s_object'],
    }

    @log_result
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        # check if this is a detail view (retrieve, update, partial_update, destroy) or not (list, create)
        if view.detail:
            # for retrieve, update, partial_update, or destroy return True
            # the permission will be checked on object level (in the next step)
            return True
        else:
            return False
