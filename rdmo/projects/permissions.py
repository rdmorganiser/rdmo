from rdmo.core.permissions import HasModelPermission, HasObjectPermission, log_result


class HasProjectsPermission(HasObjectPermission):

    @log_result
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if view.detail:
            # for retrieve, update, partial_update, the permission will be checked on the
            # object level (in the next step)
            return True

        if view.action == 'list':
            # list is allowed for every user since the filtering is done in the queryset
            return True

        if 'create' in view.action_map.values():
            # for create, check the permission (from rules.py),
            # but only if it is not a ReadOnlyValueSet (i.e. only for ProjectViewSet)
            return super().has_permission(request, view)
        else:
            return True

    @log_result
    def has_object_permission(self, request, view, obj):
        if not (request.user and request.user.is_authenticated):
            return False

        # get the project object from the obj (or the take the obj) and check its permissions
        try:
            return super().has_object_permission(request, view, obj.project)
        except AttributeError:
            return super().has_object_permission(request, view, obj)


class HasProjectPermission(HasObjectPermission):

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
            # for list or create we need to get the project from the view
            # and check that the user has the correct permission
            return super().has_object_permission(request, view, view.project)

    @log_result
    def has_object_permission(self, request, view, obj):
        if not (request.user and request.user.is_authenticated):
            return False

        # get the project object from the view (or the take the obj) and check its permissions
        return super().has_object_permission(request, view, view.project)


class HasProjectPagePermission(HasProjectPermission):

    def get_required_object_permissions(self, method, model_cls):
        return ('projects.view_page_object', )


class HasProjectProgressModelPermission(HasModelPermission):

    def get_required_permissions(self, method, model_cls):
        if method == 'POST':
            return ('projects.change_project', )
        else:
            return ('projects.view_project', )


class HasProjectProgressObjectPermission(HasProjectPermission):

    def get_required_object_permissions(self, method, model_cls):
        if method == 'POST':
            return ('projects.change_project_progress_object', )
        else:
            return ('projects.view_project_object', )


class HasProjectVisibilityModelPermission(HasModelPermission):

    def get_required_permissions(self, method, model_cls):
        if method == 'POST':
            return ('projects.change_visibility', )
        elif method == 'DELETE':
            return ('projects.delete_visibility', )
        else:
            return ('projects.view_visibility', )


class HasProjectVisibilityObjectPermission(HasProjectPermission):

    def get_required_object_permissions(self, method, model_cls):
        if method == 'POST':
            return ('projects.change_visibility_object', )
        elif method == 'DELETE':
            return ('projects.delete_visibility_object', )
        else:
            return ('projects.view_visibility_object', )
