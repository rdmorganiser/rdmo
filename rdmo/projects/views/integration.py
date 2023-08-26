import logging

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, UpdateView, View

from rdmo.core.plugins import get_plugin
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

    def get_context_data(self, **kwargs):
        kwargs['provider'] = get_plugin('PROJECT_ISSUE_PROVIDERS', self.provider_key)
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return self.project.get_absolute_url()


class IntegrationUpdateView(ObjectPermissionMixin, RedirectViewMixin, UpdateView):
    form_class = IntegrationForm
    permission_required = 'projects.change_integration_object'

    def get_queryset(self):
        return Integration.objects.filter(project_id=self.kwargs.get('project_id'))

    def get_permission_object(self):
        return self.get_object().project

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_object().project
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs['provider'] = self.get_object().provider
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return self.get_object().project.get_absolute_url()


class IntegrationDeleteView(ObjectPermissionMixin, RedirectViewMixin, DeleteView):
    permission_required = 'projects.delete_integration_object'

    def get_queryset(self):
        return Integration.objects.filter(project_id=self.kwargs.get('project_id'))

    def get_permission_object(self):
        return self.get_object().project

    def get_success_url(self):
        return self.get_object().project.get_absolute_url()


@method_decorator(csrf_exempt, name='dispatch')
class IntegrationWebhookView(View):

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        project_id = kwargs.get('project_id')

        try:
            integration = Integration.objects.filter(project_id=project_id).get(pk=pk)
            return integration.provider.webhook(request, integration)
        except Integration.DoesNotExist as e:
            raise Http404 from e
