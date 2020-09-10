import logging

from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, UpdateView

from rdmo.core.views import ObjectPermissionMixin, RedirectViewMixin
from rdmo.services.utils import get_provider, get_providers

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
        context['providers'] = get_providers(self.request)

        return context

    def post(self, request, *args, **kwargs):
        issue = self.get_object()
        provider_key = request.POST.get('send')
        provider = get_provider(request, provider_key)
        if provider:
            return provider.send_issue(issue)

        return render(request, 'core/error.html', {
            'title': _('Integration Error'),
            'errors': [_('Something went wrong. Please contact support.')]
        }, status=500)
