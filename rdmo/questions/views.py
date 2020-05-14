import logging

import defusedxml.ElementTree as ET

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView
from rdmo.core.exports import prettify_xml
from rdmo.core.imports import handle_uploaded_file, read_xml_file
from rdmo.core.utils import get_model_field_meta, render_to_format
from rdmo.core.views import CSRFViewMixin, ModelPermissionMixin

from .imports import import_questions
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


class CatalogCopyView(ModelPermissionMixin, DetailView, TemplateView):
    permission_required = ('questions.add_catalog', 'questions.change_catalog', 'questions.delete_catalog')
    model = Catalog
    context_object_name = 'catalog'
    success_url = reverse_lazy('catalogs')

    def post(self, request, *args, **kwargs):
        q = request.POST.copy()
        new_uri_prefix = q['new_uri_prefix']
        new_key = q['new_key']
        ref = request.META['HTTP_REFERER']
        source_catalog_id = ref.split('/')[-2]

        catalog = self.model.objects.get(id=source_catalog_id)
        serializer = ExportSerializer(catalog)
        xmldata = XMLRenderer().render(serializer.data)
        tree = ET.fromstring(xmldata)
        if tree is None:
            log.info('Xml parsing error. Import failed.')
            # return render(request, self.parsing_error_template, status=400)
            return HttpResponseRedirect(self.success_url)
        else:
            import_questions(tree, new_uri_prefix, new_key)
            return HttpResponseRedirect(self.success_url)
        return HttpResponseRedirect(self.success_url)


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


class CatalogImportXMLView(ModelPermissionMixin, DetailView):
    permission_required = ('questions.add_catalog', 'questions.change_catalog', 'questions.delete_catalog')
    success_url = reverse_lazy('catalogs')
    parsing_error_template = 'core/import_parsing_error.html'

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        # context = self.get_context_data(**kwargs)
        try:
            request.FILES['uploaded_file']
        except KeyError:
            return HttpResponseRedirect(self.success_url)
        else:
            tempfilename = handle_uploaded_file(request.FILES['uploaded_file'])

        tree = read_xml_file(tempfilename)
        if tree is None:
            log.info('Xml parsing error. Import failed.')
            return render(request, self.parsing_error_template, status=400)
        else:
            import_questions(tree)
            return HttpResponseRedirect(self.success_url)
