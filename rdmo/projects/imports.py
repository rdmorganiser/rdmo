import logging
import mimetypes

from rdmo.core.xml import get_ns_map, get_uri, read_xml_file
from rdmo.domain.models import Attribute
from rdmo.options.models import Option
from rdmo.questions.models import Catalog
from rdmo.tasks.models import Task
from rdmo.views.models import View

from .models import Project, Snapshot, Value

log = logging.getLogger(__name__)


class Import(object):

    def __init__(self, file_name, current_project=None):
        self.file_name = file_name
        self.current_project = current_project

        self.project = None
        self.catalog = None
        self.values = []
        self.snapshots = []
        self.tasks = []
        self.views = []

    def check(self):
        raise NotImplementedError

    def process(self):
        raise NotImplementedError


class RDMOXMLImport(Import):

    def check(self):
        file_type, encoding = mimetypes.guess_type(self.file_name)
        if file_type == 'application/xml':
            self.root = read_xml_file(self.file_name)
            if self.root and self.root.tag == 'project':
                self.ns_map = get_ns_map(self.root)
                return True

    def process(self):
        if self.current_project is None:
            catalog_uri = get_uri(self.root.find('catalog'), self.ns_map)
            try:
                self.catalog = Catalog.objects.all().get(uri=catalog_uri)
            except Catalog.DoesNotExist:
                log.info('Catalog not in db. Created with uri %s', catalog_uri)
                self.catalog = Catalog.objects.all().first()

            self.project = Project()
            self.project.title = self.root.find('title').text or ''
            self.project.description = self.root.find('description').text or ''
            self.project.created = self.root.find('created').text
            self.project.catalog = self.catalog
        else:
            self.catalog = self.current_project.catalog

        tasks_node = self.root.find('tasks')
        if tasks_node is not None:
            for task_node in tasks_node.findall('task'):
                try:
                    task_uri = get_uri(task_node, self.ns_map)
                    self.tasks.append(Task.objects.get(uri=task_uri))
                except Task.DoesNotExist:
                    pass

        views_node = self.root.find('views')
        if views_node is not None:
            for view_node in views_node.findall('view'):
                try:
                    view_uri = get_uri(view_node, self.ns_map)
                    self.views.append(View.objects.get(uri=view_uri))
                    # project.views.add(View.objects.get(uri=view_uri))
                except View.DoesNotExist:
                    pass

        values_node = self.root.find('values')
        if values_node is not None:
            for value_node in values_node.findall('value'):
                self.values.append(self.get_value(value_node))

        snapshots_node = self.root.find('snapshots')
        if snapshots_node is not None:
            for snapshot_index, snapshot_node in enumerate(snapshots_node.findall('snapshot')):
                if snapshot_node is not None:
                    snapshot = Snapshot()
                    snapshot.title = snapshot_node.find('title').text or ''
                    snapshot.description = snapshot_node.find('description').text or ''
                    snapshot.created = snapshot_node.find('created').text

                    snapshot_values = []
                    snapshot_values_node = snapshot_node.find('values')
                    if snapshot_values_node is not None:
                        for snapshot_value_node in snapshot_values_node.findall('value'):
                            snapshot_values.append(self.get_value(snapshot_value_node))

                    self.snapshots.append({
                        'index': snapshot_index,
                        'snapshot': snapshot,
                        'values': snapshot_values
                    })

    def get_value(self, value_node):
        value = Value()

        attribute_uri = get_uri(value_node.find('attribute'), self.ns_map)
        if attribute_uri is not None:
            try:
                value.attribute = Attribute.objects.get(uri=attribute_uri)
            except Attribute.DoesNotExist:
                log.info('Attribute %s not in db. Skipping.', attribute_uri)

        value.set_index = int(value_node.find('set_index').text)
        value.collection_index = int(value_node.find('collection_index').text)
        value.text = value_node.find('text').text or ''

        option_uri = get_uri(value_node.find('option'), self.ns_map)
        if option_uri is not None:
            try:
                value.option = Option.objects.get(uri=option_uri)
            except Option.DoesNotExist:
                log.info('Option %s not in db. Skipping.', option_uri)

        value_type_node = value_node.find('value_type')
        if value_type_node is not None:
            value.value_type = value_type_node.text or ''

        unit_node = value_node.find('unit')
        if unit_node is not None:
            value.unit = unit_node.text or ''

        value.created = value_node.find('created').text
        value.updated = value_node.find('updated').text

        return {
            'value': value,
            'question': value.get_question(self.catalog),
            'current': value.get_current_value(self.current_project)
        }
