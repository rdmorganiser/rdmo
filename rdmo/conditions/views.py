import logging

from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, TemplateView
from rdmo.core.exports import prettify_xml
from rdmo.core.utils import get_model_field_meta, render_to_format
from rdmo.core.views import CSRFViewMixin, ModelPermissionMixin

from .models import Condition
from .renderers import XMLRenderer
from .serializers.export import ConditionSerializer as ExportSerializer

log = logging.getLogger(__name__)


class ConditionsView(ModelPermissionMixin, CSRFViewMixin, TemplateView):
    template_name = 'conditions/conditions.html'
    permission_required = 'conditions.view_condition'

    def get_context_data(self, **kwargs):
        context = super(ConditionsView, self).get_context_data(**kwargs)
        context['export_formats'] = settings.EXPORT_FORMATS
        context['meta'] = {
            'Condition': get_model_field_meta(Condition)
        }
        return context


class ConditionsExportView(ModelPermissionMixin, ListView):
    model = Condition
    context_object_name = 'conditions'
    permission_required = 'conditions.view_condition'

    def render_to_response(self, context, **response_kwargs):
        format = self.kwargs.get('format')
        if format == 'xml':
            serializer = ExportSerializer(context['conditions'], many=True)
            xmldata = XMLRenderer().render(serializer.data)
            response = HttpResponse(prettify_xml(xmldata), content_type="application/xml")
            response['Content-Disposition'] = 'filename="conditions.xml"'
            return response
        else:
            return render_to_format(self.request, format, _('Conditions'), 'conditions/conditions_export.html', context)
