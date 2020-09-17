import logging

from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, UpdateView
from rdmo.core.views import ObjectPermissionMixin, RedirectViewMixin
from rdmo.services.utils import get_provider

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

    def get_context_data(self, **kwargs):
        kwargs['provider'] = get_provider(self.provider_key)
        return super().get_context_data(**kwargs)

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

    def get_context_data(self, **kwargs):
        kwargs['provider'] = get_provider(self.provider_key)
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return self.project.get_absolute_url()


class IntegrationDeleteView(ObjectPermissionMixin, RedirectViewMixin, DeleteView):
    model = Integration
    permission_required = 'projects.delete_integration_object'

    def get_permission_object(self):
        return self.get_object().project

    def get_success_url(self):
        return self.get_object().project.get_absolute_url()
