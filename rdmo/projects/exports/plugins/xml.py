from django.conf import settings
from django.http import HttpResponse

from rdmo.core.exports import prettify_xml

from ...renderers import XMLRenderer
from ...serializers.exports import ProjectSerializer, SnapshotSerializer
from . import Export


class XMLExport(Export):

    def render(self):
        if self.project:
            content_disposition = f'attachment; filename="{self.project.title}.xml"'
            serializer = ProjectSerializer(self.project)

        else:
            content_disposition = f'attachment; filename="{self.snapshot.title}.xml"'
            serializer = SnapshotSerializer(self.snapshot)

        xmldata = XMLRenderer().render(serializer.data)
        response = HttpResponse(prettify_xml(xmldata), content_type="application/xml")

        if settings.EXPORT_CONTENT_DISPOSITION == 'attachment':
            response['Content-Disposition'] = content_disposition

        return response
