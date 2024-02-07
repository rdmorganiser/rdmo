import hashlib
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from rules import test_rule
from rules.contrib.views import PermissionRequiredMixin as RulesPermissionRequiredMixin

from rdmo.core.views import CSRFViewMixin, PermissionRedirectMixin

logger = logging.getLogger(__name__)


class ManagementView(LoginRequiredMixin, PermissionRedirectMixin, RulesPermissionRequiredMixin,
                     CSRFViewMixin, TemplateView):
    template_name = 'management/management.html'

    def has_permission(self):
        # Use test_rule from rules for permissions check
        return test_rule('management.can_view_management', self.request.user, self.request.site)

    def render_to_response(self, context, **response_kwargs):
        storeid = hashlib.sha256(self.request.session.session_key.encode()).hexdigest()

        response = super().render_to_response(context, **response_kwargs)
        response.set_cookie('storeid', storeid)
        return response
