import logging

from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, UpdateView

from rdmo.core.views import ObjectPermissionMixin, RedirectViewMixin

from ..models import Issue

logger = logging.getLogger(__name__)


class IssueUpdateView(ObjectPermissionMixin, RedirectViewMixin, UpdateView):
    model = Issue
    queryset = Issue.objects.all()
    fields = ('status', )
    permission_required = 'projects.change_issue_object'

    def get_permission_object(self):
        return self.get_object().project


class IssueSendView(ObjectPermissionMixin, RedirectViewMixin, DetailView):
    queryset = Issue.objects.all()
    permission_required = 'projects.change_issue_object'
    template_name = 'projects/issue_send.html'

    def get_permission_object(self):
        return self.get_object().project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['integrations'] = self.get_object().project.integrations.all()

        return context

    def post(self, request, *args, **kwargs):
        issue = self.get_object()
        integration_id = request.POST.get('integration')
        integration = self.get_object().project.integrations.get(pk=integration_id)
        return integration.provider.send_issue(request, integration.options_dict, issue)
