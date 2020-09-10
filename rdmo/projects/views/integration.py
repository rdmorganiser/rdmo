import logging

from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, UpdateView

from rdmo.core.views import ObjectPermissionMixin, RedirectViewMixin

from ..forms import IntegrationForm
from ..models import Integration, Project

logger = logging.getLogger(__name__)


class IntegrationCreateView(ObjectPermissionMixin, RedirectViewMixin, CreateView):
    model = Integration
    form_class = IntegrationForm
    permission_required = 'projects.add_integration_object'

    def dispatch(self, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.all(), pk=self.kwargs['project_id'])
        self.provider_key = self.kwargs['provider_key']
        return super().dispatch(*args, **kwargs)

    def get_permission_object(self):
        return self.project

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.project
        kwargs['provider_key'] = self.provider_key
        return kwargs

    def get_success_url(self):
        return self.project.get_absolute_url()


class IntegrationUpdateView(ObjectPermissionMixin, RedirectViewMixin, UpdateView):
    model = Integration
    form_class = IntegrationForm
    permission_required = 'projects.change_integration_object'

    def dispatch(self, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.all(), pk=self.kwargs['project_id'])
        return super().dispatch(*args, **kwargs)

    def get_permission_object(self):
        return self.get_object().project

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.project
        return kwargs

    def get_success_url(self):
        return self.project.get_absolute_url()


class IntegrationDeleteView(ObjectPermissionMixin, RedirectViewMixin, DeleteView):
    model = Integration
    permission_required = 'projects.delete_integration_object'

    # def delete(self, *args, **kwargs):
    #     self.obj = self.get_object()

    #     if (self.request.user in self.obj.project.owners) or is_site_manager(self.request.user):
    #         # user is owner or site manager
    #         if is_last_owner(self.obj.project, self.obj.user):
    #             logger.info('User "%s" not allowed to remove last user "%s"', self.request.user.username, self.obj.user.username)
    #             return HttpResponseBadRequest()
    #         else:
    #             logger.info('User "%s" deletes user "%s"', self.request.user.username, self.obj.user.username)
    #             success_url = reverse('project', args=[self.get_object().project.id])
    #             self.obj.delete()
    #             return HttpResponseRedirect(success_url)

    #     elif self.request.user == self.obj.user:
    #         # user wants to remove him/herself
    #         logger.info('User "%s" deletes himself.', self.request.user.username)
    #         success_url = reverse('projects')
    #         self.obj.delete()
    #         return HttpResponseRedirect(success_url)

    #     else:
    #         logger.info('User "%s" not allowed to remove user "%s"', self.request.user.username, self.obj.user.username)
    #         return HttpResponseForbidden()

    def get_permission_object(self):
        return self.get_object().project

    def get_success_url(self):
        return self.get_object().project.get_absolute_url()
