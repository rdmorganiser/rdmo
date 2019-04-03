from django.core.exceptions import ObjectDoesNotExist

from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions


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

    def has_object_permission(self, request, view, obj):
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

    def has_permission(self, request, view):
        # check if there is a user and he/she is authenticated
        is_authenticated = request.user and request.user.is_authenticated

        # check if this is a detail view or not
        if view.detail:
            # for retrieve, update, partial_update, or destroy
            # the permission will be checked on object level
            return is_authenticated
        else:
            # for list or create we need to check the permission object from the view
            try:
                obj = view.get_permission_object()
            except (AttributeError, ObjectDoesNotExist):
                # return False if the function is not defined in the view
                # or the database query fails
                return False

            # and that the user has the correct permission on the permission filter object
            # we call the super verson of has_object_permission here!
            result = super().has_object_permission(request, view, obj)
            return is_authenticated and result

    def has_object_permission(self, request, view, obj):
        # get the permission object from the view
        try:
            obj = view.get_permission_object()
        except ObjectDoesNotExist:
            # return False if the database query fails
            return False
        except AttributeError:
            # just take the input obj if the function is not defined in the view
            pass

        result = super().has_object_permission(request, view, obj)
        return result
