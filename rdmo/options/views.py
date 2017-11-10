from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView

from rdmo.core.views import ModelPermissionMixin
from rdmo.core.utils import get_model_field_meta, render_to_format

from .models import OptionSet, Option
from .serializers.export import OptionSetSerializer as ExportSerializer
from .renderers import XMLRenderer


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
