import base64
import io
import logging
import mimetypes

from django.core.files import File
from django.http import Http404

from rest_framework.response import Response

from rdmo.core.xml import get_ns_map, get_uri, read_xml_file
from rdmo.questions.models import Catalog

from ...models import Project, Snapshot, Value
from ...serializers.imports import ProjectSerializer
from ..utils import fetch_current_project, save_project
from . import Import

logger = logging.getLogger(__name__)


class XMLImport(Import):

    accept = {
        'application/xml': ['.xml'],
        'text/xml': ['.xml'],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_name = None
        self.root = None
        self.ns_map = None

    def render(self):
        if self.file_name:
            self.session.set('file_name', self.file_name)
        else:
            self.file_name = self.session.get('file_name')

        if not self.file_name:
            raise Http404

        if self.root is None and not self.check():
            raise Http404

        self.project = self.get_project()

        fetch_current_project(self.project, self.current_project)

        serializer = ProjectSerializer(self.project)
        return Response({
            'key': self.key,
            **serializer.data
        })

    def submit(self):
        self.file_name = self.session.get('file_name')
        if not self.file_name or not self.check():
            raise Http404

        self.project = self.get_project()

        fetch_current_project(self.project, self.current_project)

        save_project(self.project)

        return Response({})

    def check(self):
        file_type, _encoding = mimetypes.guess_type(self.file_name)
        if self.accept and file_type in self.accept:
            self.root = read_xml_file(self.file_name)
            if self.root is not None and self.root.tag == 'project':
                self.ns_map = get_ns_map(self.root)
                return True
        return False

    def get_project(self):
        project = Project()
        project.title = self.get_title()
        project.description = self.get_description()
        project.created = self.get_created()
        project.updated = self.get_updated()
        project.catalog = self.get_catalog()
        project._values = self.get_values()
        project._snapshots = self.get_snapshots()

        return project

    def get_title(self):
        return self.root.find('title').text or ''

    def get_description(self):
        return self.root.find('description').text or ''

    def get_created(self):
        return self.root.find('created').text or self.now

    def get_updated(self):
        return self.now

    def get_catalog(self):
        catalog_uri = get_uri(self.root.find('catalog'), self.ns_map)

        available_catalogs = Catalog.objects.filter_for_user(self.request.user)

        try:
            return available_catalogs.get(uri=catalog_uri)
        except Catalog.DoesNotExist:
            logger.info('Catalog with uri %s does not exists. Used first available catalog.', catalog_uri)
            return available_catalogs.first()

    def get_values(self):
        values_node = self.root.find('values')
        if values_node is not None:
            return [
                self.get_value(value_node)
                for value_node in values_node.findall('value')
            ]
        else:
            return []

    def get_snapshots(self):
        snapshots_node = self.root.find('snapshots')
        if snapshots_node is not None:
            return [
                self.get_snapshot(snapshot_index, snapshot_node)
                for snapshot_index, snapshot_node in enumerate(snapshots_node.findall('snapshot'))
            ]
        else:
            return []

    def get_snapshot(self, snapshot_index, snapshot_node):
        snapshot = Snapshot()
        snapshot.title = self.get_snapshot_title(snapshot_node)
        snapshot.description = self.get_snapshot_description(snapshot_node)
        snapshot.created = self.get_snapshot_created(snapshot_node)
        snapshot.updated = self.get_snapshot_updated(snapshot_node)

        snapshot._index = snapshot_index
        snapshot._values = self.get_snapshot_values(snapshot_node)

        return snapshot

    def get_snapshot_title(self, snapshot_node):
        return snapshot_node.find('title').text or ''

    def get_snapshot_description(self, snapshot_node):
        return snapshot_node.find('description').text or ''

    def get_snapshot_created(self, snapshot_node):
        return snapshot_node.find('created').text or self.now

    def get_snapshot_updated(self, snapshot_node):
        return self.now

    def get_snapshot_values(self, snapshot_node):
        snapshot_values_node = snapshot_node.find('values')
        if snapshot_values_node is not None:
            return [
                self.get_value(value_node)
                for value_node in snapshot_values_node.findall('value')
            ]
        else:
            return []

    def get_value(self, value_node):
        value = Value()
        value.attribute = self.get_value_attribute(value_node)
        value.set_prefix = self.get_value_set_prefix(value_node)
        value.set_index = self.get_value_set_index(value_node)
        value.set_collection = self.get_value_set_collection(value_node)
        value.collection_index = self.get_value_collection_index(value_node)
        value.text = self.get_value_text(value_node)
        value.option = self.get_value_option(value_node)
        value.external_id = self.get_value_external_id(value_node)
        value._file_name, value._file = self.get_value_file(value_node)
        value.value_type = self.get_value_value_type(value_node)
        value.unit = self.get_value_unit(value_node)
        value.created = self.get_value_created(value_node)
        value.updated = self.get_value_updated(value_node)
        return value

    def get_value_attribute(self, value_node):
        attribute_uri = get_uri(value_node.find('attribute'), self.ns_map)
        if attribute_uri is not None:
            return self.attributes.get(attribute_uri)

    def get_value_set_prefix(self, value_node):
        try:
            return value_node.find('set_prefix').text or ''
        except AttributeError:
            return ''

    def get_value_set_index(self, value_node):
        return int(value_node.find('set_index').text)

    def get_value_set_collection(self, value_node):
        try:
            set_collection_text = value_node.find('set_collection').text
            if set_collection_text == 'True':
                return True
            elif set_collection_text == 'False':
                return False
            else:
                return None
        except AttributeError:
            return None

    def get_value_collection_index(self, value_node):
        return int(value_node.find('collection_index').text)

    def get_value_text(self, value_node):
        return value_node.find('text').text or ''

    def get_value_option(self, value_node):
        option_uri = get_uri(value_node.find('option'), self.ns_map)
        if option_uri:
            return self.options.get(option_uri)

    def get_value_file(self, value_node):
        file_node = value_node.find('file')
        if file_node is not None:
            file_string = file_node.text
            if file_string is not None:
                return (
                    file_node.attrib.get('name', 'file.dat'),
                    File(io.BytesIO(base64.b64decode(file_string)))
                )
        return (None, None)

    def get_value_external_id(self, value_node):
        external_id_node = value_node.find('external_id')
        if external_id_node is not None:
            return external_id_node.text or ''

    def get_value_value_type(self, value_node):
        value_type_node = value_node.find('value_type')
        if value_type_node is not None:
            return value_type_node.text or ''

    def get_value_unit(self, value_node):
        unit_node = value_node.find('unit')
        if unit_node is not None:
            return unit_node.text or ''

    def get_value_created(self, value_node):
        return value_node.find('created').text or self.now

    def get_value_updated(self, value_node):
        return value_node.find('updated').text or self.now
