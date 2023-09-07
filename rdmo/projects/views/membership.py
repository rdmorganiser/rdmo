import logging

from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DeleteView, UpdateView
from django.views.generic.edit import FormView

from rdmo.accounts.utils import is_site_manager
from rdmo.core.views import ObjectPermissionMixin, RedirectViewMixin

from ..forms import MembershipCreateForm
from ..models import Membership, Project
from ..utils import is_last_owner, send_invite_email

logger = logging.getLogger(__name__)


class MembershipCreateView(ObjectPermissionMixin, RedirectViewMixin, FormView):
    model = Membership
    form_class = MembershipCreateForm
    permission_required = 'projects.add_membership_object'
    template_name = 'projects/membership_form.html'

    def dispatch(self, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.all(), pk=self.kwargs['project_id'])
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return Membership.objects.filter(project=self.project)

    def get_permission_object(self):
        return self.project

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.project
        kwargs['is_site_manager'] = is_site_manager(self.request.user)
        return kwargs

    def get_success_url(self):
        return self.project.get_absolute_url()

    def form_valid(self, form):
        invite = form.save()
        if invite is not None and settings.PROJECT_SEND_INVITE:
            send_invite_email(self.request, invite)
        return super().form_valid(form)


class MembershipUpdateView(ObjectPermissionMixin, RedirectViewMixin, UpdateView):
    fields = ('role', )
    permission_required = 'projects.change_membership_object'

    def get_queryset(self):
        return Membership.objects.filter(project_id=self.kwargs.get('project_id'))

    def get_permission_object(self):
        return self.get_object().project


class MembershipDeleteView(ObjectPermissionMixin, RedirectViewMixin, DeleteView):
    permission_required = 'projects.delete_membership_object'

    def get_queryset(self):
        return Membership.objects.filter(project_id=self.kwargs.get('project_id'))

    def form_valid(self, form):
        self.obj = self.get_object()

        if (self.request.user in self.obj.project.owners) or is_site_manager(self.request.user):
            # user is owner or site manager
            if is_last_owner(self.obj.project, self.obj.user):
                logger.info('User "%s" not allowed to remove last user "%s"',
                            self.request.user.username, self.obj.user.username)
                return HttpResponseBadRequest()
            else:
                logger.info('User "%s" deletes user "%s"', self.request.user.username, self.obj.user.username)
                success_url = reverse('project', args=[self.get_object().project.id])
                self.obj.delete()
                return HttpResponseRedirect(success_url)

        elif self.request.user == self.obj.user:
            # user wants to remove him/herself
            logger.info('User "%s" deletes himself.', self.request.user.username)
            success_url = reverse('projects')
            self.obj.delete()
            return HttpResponseRedirect(success_url)

        else:
            logger.info('User "%s" not allowed to remove user "%s"', self.request.user.username, self.obj.user.username)
            return HttpResponseForbidden()

    def get_permission_object(self):
        return self.get_object().project
