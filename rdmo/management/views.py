import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from rules.contrib.views import PermissionRequiredMixin as RulesPermissionRequiredMixin

from rdmo.core.views import CSRFViewMixin, PermissionRedirectMixin, StoreIdViewMixin

logger = logging.getLogger(__name__)


class ManagementView(LoginRequiredMixin, PermissionRedirectMixin, RulesPermissionRequiredMixin,
                     CSRFViewMixin, StoreIdViewMixin, TemplateView):
    template_name = 'management/management.html'
    permission_required = 'management.view_management'
