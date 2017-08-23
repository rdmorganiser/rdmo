from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView

from rdmo.core.views import ModelPermissionMixin
from rdmo.core.utils import get_model_field_meta, render_to_format, render_to_csv

from .models import AttributeEntity, Attribute, VerboseName, Range
from .serializers.export import AttributeEntitySerializer as ExportSerializer
from .renderers import XMLRenderer


class DomainView(ModelPermissionMixin, TemplateView):
    template_name = 'domain/domain.html'
    permission_required = 'domain.view_attributeentity'

    def get_context_data(self, **kwargs):
        context = super(DomainView, self).get_context_data(**kwargs)
        context['export_formats'] = settings.EXPORT_FORMATS
        context['meta'] = {
            'Attribute': get_model_field_meta(Attribute),
            'VerboseName': get_model_field_meta(VerboseName),
            'Range': get_model_field_meta(Range)
        }
        return context


class DomainExportView(ModelPermissionMixin, ListView):
    model = AttributeEntity
    context_object_name = 'entities'
    permission_required = 'domain.view_attributeentity'

    def get_queryset(self):
        if self.kwargs.get('format') == 'xml':
            return AttributeEntity.objects.filter(parent=None)
        else:
            return AttributeEntity.objects.all()

    def render_to_response(self, context, **response_kwargs):
        format = self.kwargs.get('format')
        if format == 'xml':
            serializer = ExportSerializer(context['entities'], many=True)
            response = HttpResponse(XMLRenderer().render(serializer.data), content_type="application/xml")
            response['Content-Disposition'] = 'filename="domain.xml"'
            return response
        elif format == 'csv':
            rows = []
            for entity in context['entities']:
                rows.append((
                    _('Attribute') if entity.is_attribute else _('Entity'),
                    _('collection') if entity.is_collection else '',
                    entity.key,
                    entity.comment,
                    entity.uri,
                    entity.attribute.value_type if entity.is_attribute else '',
                    entity.attribute.unit if entity.is_attribute else ''
                ))
            return render_to_csv(self.request, _('Domain'), rows)
        else:
            return render_to_format(self.request, format, _('Domain'), 'domain/domain_export.html', context)
