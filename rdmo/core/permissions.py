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

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        # check if this is a detail view (retrieve, update, partial_update, destroy) or not (list, create)
        if view.detail:
            # for retrieve, update, partial_update, or destroy return True
            # the permission will be checked on object level (in the next step)
            return True
        else:
            try:
                # for list or create we need to check the permission object from the view
                # and check that the user has the correct permission on this object
                permission_object = view.get_list_permission_object()
                return super().has_object_permission(request, view, permission_object)
            except ObjectDoesNotExist:
                # return False if the database query fails
                return False
            except AttributeError:
                # return True if the function is not defined in the view
                # the permission will be checked on object level (in the next step)
                return True

    def has_object_permission(self, request, view, obj):
        # get the permission object from the view
        try:
            permission_object = view.get_detail_permission_object(obj)
            return super().has_object_permission(request, view, permission_object)
        except ObjectDoesNotExist:
            # return False if the database query fails
            return False
        except AttributeError:
            # just take the input obj if the function is not defined in the view
            return super().has_object_permission(request, view, obj)
