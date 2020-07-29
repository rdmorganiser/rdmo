import logging

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, TemplateView

from rdmo.core.exports import prettify_xml
from rdmo.core.imports import handle_uploaded_file, read_xml_file
from rdmo.core.utils import get_model_field_meta, render_to_format
from rdmo.core.views import CSRFViewMixin, ModelPermissionMixin

from .imports import import_conditions
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


class ConditionsImportXMLView(ModelPermissionMixin, ListView):
    permission_required = ('conditions.add_condition', 'conditions.change_condition', 'conditions.delete_condition')
    success_url = reverse_lazy('conditions')

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
            import_conditions(tree)
            return HttpResponseRedirect(self.success_url)
