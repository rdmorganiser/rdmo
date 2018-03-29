import logging

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView

from rdmo.core.imports import handle_uploaded_file, validate_xml
from rdmo.core.utils import get_model_field_meta, render_to_format
from rdmo.core.views import ModelPermissionMixin

from .imports import import_conditions
from .models import Condition
from .serializers.export import ConditionSerializer as ExportSerializer
from .renderers import XMLRenderer

log = logging.getLogger(__name__)


class ConditionsView(ModelPermissionMixin, TemplateView):
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
            response = HttpResponse(XMLRenderer().render(serializer.data), content_type="application/xml")
            response['Content-Disposition'] = 'filename="conditions.xml"'
            return response
        else:
            return render_to_format(self.request, format, _('Conditions'), 'conditions/conditions_export.html', context)


class ConditionsImportXMLView(ModelPermissionMixin, ListView):
    permission_required = 'projects.export_project_object'
    success_url = '/conditions'
    template_name = 'conditions/file_upload.html'

    def get(self, request, *args, **kwargs):
        form = UploadFileForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # context = self.get_context_data(**kwargs)
        tempfilename = handle_uploaded_file(request.FILES['uploaded_file'])
        roottag, xmltree = validate_xml(tempfilename)
        if roottag == 'conditions':
            import_conditions(xmltree)
            return HttpResponseRedirect(self.success_url)
        else:
            log.info('Xml parsing error. Import failed.')
            return HttpResponse('Xml parsing error. Import failed.')
