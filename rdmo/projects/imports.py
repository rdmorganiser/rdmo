import logging
import mimetypes

from django.contrib.sites.models import Site

from rdmo.core.xml import get_ns_map, get_uri, read_xml_file
from rdmo.domain.models import Attribute
from rdmo.options.models import Option
from rdmo.questions.models import Catalog
from rdmo.tasks.models import Task
from rdmo.views.models import View

from .models import Project, Snapshot, Value

log = logging.getLogger(__name__)


class Import(object):

    def __init__(self, file_name, project=None, snapshot=None):
        self.file_name = file_name
        self.project = project
        self.snapshot = snapshot

    def check(self):
        raise NotImplementedError

    def process(self, save=None):
        raise NotImplementedError


class RDMOXMLImport(Import):

    def check(self):
        if mimetypes.guess_type('application/xml'):
            self.root = read_xml_file(self.file_name)
            self.ns_map = get_ns_map(self.root)

            if self.root and self.root.tag == 'project':
                return True

    def process(self):
        project = Project()
        project.title = self.root.find('title').text or ''
        project.description = self.root.find('description').text or ''
        project.created = self.root.find('created').text
        project.site = Site.objects.get_current()

        catalog = get_uri(self.root.find('catalog'), self.ns_map)

        try:
            project.catalog = Catalog.objects.all().get(uri=catalog)
        except Catalog.DoesNotExist:
            log.info('Catalog not in db. Created with uri %s', catalog)
            project.catalog = Catalog.objects.all().first()

        tasks = []
        tasks_node = self.root.find('tasks')
        if tasks_node is not None:
            for task_node in tasks_node.findall('task'):
                try:
                    task_uri = get_uri(task_node, self.ns_map)
                    tasks.append(Task.objects.get(uri=task_uri))
                except Task.DoesNotExist:
                    pass

        views = []
        views_node = self.root.find('views')
        if views_node is not None:
            for view_node in views_node.findall('view'):
                try:
                    view_uri = get_uri(view_node, self.ns_map)
                    views.append(View.objects.get(uri=view_uri))
                    # project.views.add(View.objects.get(uri=view_uri))
                except View.DoesNotExist:
                    pass

        values = []
        values_node = self.root.find('values')
        if values_node is not None:
            for value_node in values_node.findall('value'):
                value = self.import_value(value_node, project)
                if value is not None:
                    values.append(value)

        snapshots = []
        snapshots_node = self.root.find('snapshots')
        if snapshots_node is not None:
            for snapshot_index, snapshot_node in enumerate(snapshots_node.findall('snapshot')):
                if snapshot_node is not None:
                    snapshot = Snapshot()
                    snapshot.project = project
                    snapshot.title = snapshot_node.find('title').text or ''
                    snapshot.description = snapshot_node.find('description').text or ''
                    snapshot.created = snapshot_node.find('created').text

                    snapshot_values = []
                    snapshot_values_node = snapshot_node.find('values')
                    if snapshot_values_node is not None:
                        for snapshot_value_node in snapshot_values_node.findall('value'):
                            snapshot_value = self.import_value(snapshot_value_node, project, snapshot)
                            if snapshot_value is not None:
                                snapshot_values.append(snapshot_value)

                    snapshots.append({
                        'index': snapshot_index,
                        'snapshot': snapshot,
                        'values': snapshot_values
                    })

        return project, values, snapshots, tasks, views

    def import_value(self, value_node, project, snapshot=None):
        value = Value()
        value.project = project
        value.snapshot = snapshot

        attribute_uri = get_uri(value_node.find('attribute'), self.ns_map)
        if attribute_uri is not None:
            try:
                value.attribute = Attribute.objects.get(uri=attribute_uri)
            except Attribute.DoesNotExist:
                log.info('Attribute %s not in db. Skipping.', attribute_uri)

        value.set_index = value_node.find('set_index').text
        value.collection_index = value_node.find('collection_index').text
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

        return value
