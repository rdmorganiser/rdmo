import logging

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy

from rdmo.core.imports import handle_uploaded_file, validate_xml
from rdmo.core.views import ModelPermissionMixin
from rdmo.core.utils import get_model_field_meta, render_to_format

from .imports import import_options
from .models import OptionSet, Option
from .serializers.export import OptionSetSerializer as ExportSerializer
from .renderers import XMLRenderer

log = logging.getLogger(__name__)


class OptionsView(ModelPermissionMixin, TemplateView):
    template_name = 'options/options.html'
    permission_required = 'options.view_option'

    def get_context_data(self, **kwargs):
        context = super(OptionsView, self).get_context_data(**kwargs)
        context['export_formats'] = settings.EXPORT_FORMATS
        context['meta'] = {
            'OptionSet': get_model_field_meta(OptionSet),
            'Option': get_model_field_meta(Option)
        }
        return context


class OptionsExportView(ModelPermissionMixin, ListView):
    model = OptionSet
    context_object_name = 'optionsets'
    permission_required = 'options.view_option'

    def render_to_response(self, context, **response_kwargs):
        format = self.kwargs.get('format')
        if format == 'xml':
            serializer = ExportSerializer(context['optionsets'], many=True)
            response = HttpResponse(XMLRenderer().render(serializer.data), content_type="application/xml")
            response['Content-Disposition'] = 'filename="options.xml"'
            return response
        else:
            return render_to_format(self.request, format, _('Options'), 'options/options_export.html', context)


class OptionsImportXMLView(ModelPermissionMixin, ListView):
    permission_required = ('options.add_option', 'options.change_option', 'options.delete_option')
    success_url = reverse_lazy('options')
    parsing_error_template = 'core/import_parsing_error.html'

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        try:
            request.FILES['uploaded_file']
        except:
            return HttpResponseRedirect(self.success_url)
        else:
            tempfilename = handle_uploaded_file(request.FILES['uploaded_file'])

        roottag, xmltree = validate_xml(tempfilename)
        if roottag == 'options':
            import_options(xmltree)
            return HttpResponseRedirect(self.success_url)
        else:
            log.info('Xml parsing error. Import failed.')
            return render(request, self.parsing_error_template, status=400)
