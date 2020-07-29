import logging

from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, TemplateView

from rdmo.core.exports import prettify_xml
from rdmo.core.utils import get_model_field_meta, render_to_format
from rdmo.core.views import CSRFViewMixin, ModelPermissionMixin

from .models import View
from .renderers import XMLRenderer
from .serializers.export import ViewSerializer as ExportSerializer

log = logging.getLogger(__name__)


class ViewsView(ModelPermissionMixin, CSRFViewMixin, TemplateView):
    template_name = 'views/views.html'
    permission_required = 'views.view_view'

    def get_context_data(self, **kwargs):
        context = super(ViewsView, self).get_context_data(**kwargs)
        context['export_formats'] = settings.EXPORT_FORMATS
        context['meta'] = {
            'View': get_model_field_meta(View)
        }
        return context


class ViewsExportView(ModelPermissionMixin, ListView):
    model = View
    context_object_name = 'views'
    permission_required = 'views.view_view'

    def render_to_response(self, context, **response_kwargs):
        format = self.kwargs.get('format')
        if format == 'xml':
            serializer = ExportSerializer(context['views'], many=True)
            xmldata = XMLRenderer().render(serializer.data)
            response = HttpResponse(prettify_xml(xmldata), content_type="application/xml")
            response['Content-Disposition'] = 'filename="views.xml"'
            return response
        else:
            return render_to_format(self.request, format, _('Views'), 'views/views_export.html', context)
