import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from rdmo.core.views import CSRFViewMixin

logger = logging.getLogger(__name__)


class ManagementView(LoginRequiredMixin, CSRFViewMixin, TemplateView):
    template_name = 'management/management.html'
