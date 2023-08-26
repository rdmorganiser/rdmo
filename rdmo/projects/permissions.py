from rdmo.core.permissions import HasObjectPermission, log_result


class HasProjectsPermission(HasObjectPermission):

    @log_result
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        # always return True:
        # for retrieve, update, partial_update, the permission will be checked on the
        # object level (in the next step), list and create is allowed for every user since
        # the filtering is done in the queryset
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
            try:
                return super().has_object_permission(request, view, view.project)
            except AttributeError:  # needed for swagger /api/v1
                return super().has_permission(request, view)

    @log_result
    def has_object_permission(self, request, view, obj):
        if not (request.user and request.user.is_authenticated):
            return False

        # get the project object from the view (or the take the obj) and check its permissions
        try:
            return super().has_object_permission(request, view, view.project)
        except AttributeError:
            return super().has_object_permission(request, view, obj)


class HasProjectPagePermission(HasProjectPermission):

    def get_required_object_permissions(self, method, model_cls):
        return ('projects.view_page_object', )
