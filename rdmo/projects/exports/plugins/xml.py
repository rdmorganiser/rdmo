from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from rdmo.core.exports import prettify_xml

from ...renderers import XMLRenderer
from ...serializers.exports import ProjectSerializer, SnapshotSerializer
from . import Export


class XMLExportMixin:
    def get_serialiser(self):
        if self.project:
            return ProjectSerializer(self.project)
        else:
            return SnapshotSerializer(self.snapshot)

    def get_content_disposition(self):
        if settings.EXPORT_CONTENT_DISPOSITION == 'attachment':
            if self.project:
                return f'attachment; filename="{self.project.title}.xml"'
            else:
                return f'attachment; filename="{self.snapshot.title}.xml"'

    def get_response(self, xml):
        response = HttpResponse(prettify_xml(xml), content_type="application/xml")
        if content_disposition := self.get_content_disposition():
            response['Content-Disposition'] = content_disposition
        return response


class XMLExport(XMLExportMixin, Export):
    label = _('RDMO XML')
    description = _('Export the project including its snapshots as an RDMO XML file, '
                    'which can be imported into this or another RDMO instance.')
    download = True

    def render(self):
        serializer = self.get_serialiser()
        xml = XMLRenderer().render(serializer.data)
        return self.get_response(xml)
