import logging

from django.views.generic import DeleteView

from rdmo.core.views import ObjectPermissionMixin, RedirectViewMixin

from ..models import Invite

logger = logging.getLogger(__name__)


class InviteDeleteView(ObjectPermissionMixin, RedirectViewMixin, DeleteView):
    permission_required = 'projects.delete_invite_object'

    def get_queryset(self):
        return Invite.objects.filter(project_id=self.kwargs.get('project_id'))

    def get_permission_object(self):
        return self.get_object().project

    def get_success_url(self):
        return self.get_object().project.get_absolute_url()
