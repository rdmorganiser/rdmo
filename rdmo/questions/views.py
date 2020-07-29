import logging

from django.conf import settings
from django.http import HttpResponse
from django.views.generic import DetailView, TemplateView
from rdmo.core.exports import prettify_xml
from rdmo.core.utils import get_model_field_meta, render_to_format
from rdmo.core.views import CSRFViewMixin, ModelPermissionMixin

from .models import Catalog, Question, QuestionSet, Section
from .renderers import XMLRenderer
from .serializers.export import CatalogSerializer as ExportSerializer

log = logging.getLogger(__name__)


class CatalogsView(ModelPermissionMixin, CSRFViewMixin, TemplateView):
    template_name = 'questions/catalogs.html'
    permission_required = 'questions.view_catalog'

    def get_context_data(self, **kwargs):
        context = super(CatalogsView, self).get_context_data(**kwargs)
        context['export_formats'] = settings.EXPORT_FORMATS
        context['meta'] = {
            'Catalog': get_model_field_meta(Catalog),
            'Section': get_model_field_meta(Section),
            'QuestionSet': get_model_field_meta(QuestionSet),
            'Question': get_model_field_meta(Question),
        }
        return context


class CatalogExportView(ModelPermissionMixin, DetailView):
    model = Catalog
    context_object_name = 'catalog'
    permission_required = 'questions.view_catalog'

    def render_to_response(self, context, **response_kwargs):
        format = self.kwargs.get('format')
        if format == 'xml':
            serializer = ExportSerializer(context['catalog'])
            xmldata = XMLRenderer().render(serializer.data)
            response = HttpResponse(prettify_xml(xmldata), content_type="application/xml")
            response['Content-Disposition'] = 'filename="%s.xml"' % context['catalog'].key
            return response
        else:
            return render_to_format(self.request, format, context['catalog'].title, 'questions/catalog_export.html', context)
