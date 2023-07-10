import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from rules import test_rule
from rules.contrib.views import PermissionRequiredMixin as RulesPermissionRequiredMixin

from rdmo.core.views import CSRFViewMixin, PermissionRedirectMixin

logger = logging.getLogger(__name__)


class ManagementView(LoginRequiredMixin, PermissionRedirectMixin, RulesPermissionRequiredMixin, CSRFViewMixin, TemplateView):
    template_name = 'management/management.html'
    permission_required = 'management.can_view_management'

    def has_permission(self):
        """
        use test_rule from rules for permissions check
        """
        perms = self.get_permission_required()
        return all(map(lambda perm: test_rule(perm, self.request.user, self.request.site), perms))
