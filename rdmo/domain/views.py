import logging
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView

from rdmo.core.imports import handle_uploaded_file, validate_xml
from rdmo.domain.imports import import_domain
from rdmo.core.views import ModelPermissionMixin, ObjectPermissionMixin
from rdmo.core.utils import get_model_field_meta, render_to_format, render_to_csv

from .forms import UploadFileForm
from .models import AttributeEntity, Attribute, Range, VerboseName
from .serializers.export import AttributeEntitySerializer as ExportSerializer
from .renderers import XMLRenderer

log = logging.getLogger(__name__)


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


class DomainImportXMLView(ObjectPermissionMixin, TemplateView):
    # model = Project
    permission_required = 'projects.export_project_object'
    # form_class = ProjectForm
    success_url = '/'
    template_name = 'projects/project_upload.html'

    def get(self, request, *args, **kwargs):
        form = UploadFileForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # context = self.get_context_data(**kwargs)
        tempfilename = handle_uploaded_file(request.FILES['uploaded_file'])
        exit_code, xmltree = validate_xml(tempfilename, 'project')
        if exit_code == 0:
            self.importProject(xmltree, request)
            return HttpResponseRedirect(self.success_url)
        else:
            log.info('Xml parsing error. Import failed.')
            return HttpResponse('Xml parsing error. Import failed.')

    def form_valid(self, form, request, *args, **kwargs):
        form.save(commit=True)
        messages.success(request, 'File uploaded!')
        # return super(ProjectImportXMLView, self).form_valid(form)
        return

    def importProject(self, xml_root, request):
        try:
            user = request.user
        except User.DoesNotExist:
            log.info('Unable to detect user name. Import failed.')
        else:
            import_domain(xml_root, user)
