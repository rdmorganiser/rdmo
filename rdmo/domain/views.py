import logging

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, TemplateView

from rdmo.core.exports import prettify_xml
from rdmo.core.imports import handle_uploaded_file, read_xml_file
from rdmo.core.utils import (get_model_field_meta, render_to_csv,
                             render_to_format)
from rdmo.core.views import (CSRFViewMixin, ModelPermissionMixin,
                             ObjectPermissionMixin)
from rdmo.domain.imports import import_domain

from .models import Attribute
from .renderers import XMLRenderer
from .serializers.export import AttributeSerializer as ExportSerializer

log = logging.getLogger(__name__)


class DomainView(ModelPermissionMixin, CSRFViewMixin, TemplateView):
    template_name = 'domain/domain.html'
    permission_required = 'domain.view_attribute'

    def get_context_data(self, **kwargs):
        context = super(DomainView, self).get_context_data(**kwargs)
        context['export_formats'] = settings.EXPORT_FORMATS
        context['meta'] = {
            'Attribute': get_model_field_meta(Attribute)
        }
        return context


class DomainExportView(ModelPermissionMixin, ListView):
    model = Attribute
    context_object_name = 'attributes'
    permission_required = 'domain.view_attribute'

    def render_to_response(self, context, **response_kwargs):
        format = self.kwargs.get('format')
        if format == 'xml':
            queryset = Attribute.objects.get_cached_trees()
            serializer = ExportSerializer(queryset, many=True)
            xmldata = XMLRenderer().render(serializer.data)
            response = HttpResponse(prettify_xml(xmldata), content_type="application/xml")
            response['Content-Disposition'] = 'filename="domain.xml"'
            return response
        elif format[:3] == 'csv':
            if format == 'csvcomma':
                delimiter = ','
            else:
                delimiter = ';'
            rows = []
            for attribute in context['attributes']:
                rows.append((
                    attribute.key,
                    attribute.comment,
                    attribute.uri
                ))
            return render_to_csv(_('Domain'), rows, delimiter)
        else:
            return render_to_format(self.request, format, _('Domain'), 'domain/domain_export.html', context)


class DomainImportXMLView(ObjectPermissionMixin, TemplateView):
    permission_required = ('domain.add_attribute', 'domain.change_attribute', 'domain.delete_attribute')
    success_url = reverse_lazy('domain')

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        try:
            request.FILES['uploaded_file']
        except KeyError:
            return HttpResponseRedirect(self.success_url)
        else:
            tempfilename = handle_uploaded_file(request.FILES['uploaded_file'])

        tree = read_xml_file(tempfilename)
        if tree is None:
            log.info('Xml parsing error. Import failed.')
            return render(request, 'core/error.html', {
                'title': _('Import error'),
                'error': _('The content of the xml file does not consist of well formed data or markup.')
            }, status=400)
        else:
            import_domain(tree)
            return HttpResponseRedirect(self.success_url)
