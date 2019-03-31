import logging

from rdmo.core.xml import get_ns_map, get_uri
from rdmo.questions.models import Catalog
from rdmo.domain.models import Attribute
from rdmo.options.models import Option

from .models import Membership, Project, Snapshot, Value

log = logging.getLogger(__name__)


def import_project(user, root):
    ns_map = get_ns_map(root)

    project = Project()

    project.title = root.find('title').text or ''
    project.description = root.find('description').text or ''
    project.created = root.find('created').text

    catalog = get_uri(root.find('catalog'), ns_map)

    try:
        project.catalog = Catalog.objects.get(uri=catalog)
    except Catalog.DoesNotExist:
        log.info('Catalog not in db. Created with uri %s', catalog)
        project.catalog = Catalog.objects.first()

    project.save()

    # add user to project
    membership = Membership(project=project, user=user, role='owner')
    membership.save()

    snapshots_node = root.find('snapshots')
    if snapshots_node is not None:
        for snapshot_node in snapshots_node.findall('snapshot'):
            if snapshot_node is not None:
                snapshot = Snapshot()
                snapshot.project = project
                snapshot.title = snapshot_node.find('title').text or ''
                snapshot.description = snapshot_node.find('description').text or ''
                snapshot.created = snapshot_node.find('created').text
                snapshot.save()

                snapshot_values_node = snapshot_node.find('values')
                if snapshot_values_node is not None:
                    for snapshot_value_node in snapshot_values_node.findall('value'):
                        import_value(snapshot_value_node, ns_map, project, snapshot)

    values_node = root.find('values')
    if values_node is not None:
        for value_node in values_node.findall('value'):
            import_value(value_node, ns_map, project)


def import_value(value_node, ns_map, project, snapshot=None):
    value = Value()

    value.project = project
    value.snapshot = snapshot

    attribute_uri = get_uri(value_node.find('attribute'), ns_map)
    if attribute_uri is not None:
        try:
            value.attribute = Attribute.objects.get(uri=attribute_uri)
        except Attribute.DoesNotExist:
            log.info('Attribute %s not in db. Skipping.', attribute_uri)
            return

    value.set_index = value_node.find('set_index').text
    value.collection_index = value_node.find('collection_index').text
    value.text = value_node.find('text').text or ''

    option_uri = get_uri(value_node.find('option'), ns_map)
    if option_uri is not None:
        try:
            value.option = Option.objects.get(uri=option_uri)
        except Option.DoesNotExist:
            log.info('Option %s not in db. Skipping.', option_uri)
            return

    value_type_node = value_node.find('value_type')
    if value_type_node is not None:
        value.value_type = value_type_node.text or ''

    unit_node = value_node.find('unit')
    if unit_node is not None:
        value.unit = unit_node.text or ''

    value.created = value_node.find('created').text
    value.updated = value_node.find('updated').text

    value.save()
