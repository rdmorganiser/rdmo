import logging

from rdmo.core.imports import get_value_from_treenode
from rdmo.core.utils import get_ns_map, get_ns_tag
from rdmo.domain.models import Attribute
from rdmo.options.models import Option
from rdmo.questions.models import Catalog

from .models import Project, Membership, Snapshot, Value


log = logging.getLogger(__name__)


def import_project(project_node, user):
    log.info('Importing project')
    nsmap = get_ns_map(project_node.getroot())
    project_title = get_value_from_treenode(project_node, 'title')
    project_created = project_node.find('created').text
    project_description = get_value_from_treenode(project_node, 'description')

    log.info('Creating new project "' + str(project_title) + '".')
    project = Project(title=project_title)

    try:
        project_catalog = project_node.find('catalog')
        catalog_uri = project_catalog.get(get_ns_tag('dc:uri', nsmap))
        project.catalog = Catalog.objects.get(uri=catalog_uri)
    except Catalog.DoesNotExist:
        project.catalog = Catalog.objects.first()
        log.info('Project catalog not in db. Created with uri "' + str(catalog_uri) + '".')
    else:
        log.info('Project catalog does exist. Loaded from uri ' + str(catalog_uri))

    if project_description:
        project.description = project_description
    else:
        project.description = ''

    project.created = project_created
    log.info('Project saving with title "' + str(project_title) + '"')
    project.save()

    # add user to project
    membership = Membership(project=project, user=user, role='owner')
    membership.save()

    # loop over snapshots
    try:
        for snapshot_node in project_node.find('snapshots').iter('snapshot'):
            import_snapshot(snapshot_node, nsmap, project)
    except AttributeError:
        log.error(str(AttributeError))
        pass

    loop_over_values(project_node, nsmap, project)


def import_snapshot(snapshot_node, nsmap, project):
    snapshot = Snapshot(project=project, title=get_value_from_treenode(snapshot_node, 'title'))

    snapshot_description = get_value_from_treenode(snapshot_node, 'description')
    if snapshot_description:
        snapshot.description = snapshot_description
    else:
        snapshot.description = ''

    snapshot.created = snapshot_node.find('created').text
    snapshot.save()

    loop_over_values(snapshot_node, nsmap, project, snapshot)


def loop_over_values(parentnode, nsmap, project, snapshot=None):
    try:
        for childnode in parentnode.iter():
            import_value(childnode, nsmap, project)
    except AttributeError:
        log.error(str(AttributeError))
        pass


def import_value(value_node, nsmap, project, snapshot=None):
    log.info('Importing value node: ' + str(value_node))
    attribute_uri = get_value_from_treenode(value_node, 'title')

    if attribute_uri is not None:
        try:
            attribute = Attribute.objects.get(uri=attribute_uri)
        except Attribute.DoesNotExist:
            log.info('Skipping value for Attribute "%s". Attribute not found.' % attribute_uri)
            return

        try:
            value = Value.objects.get(
                project=project,
                snapshot=snapshot,
                attribute=attribute,
                set_index=get_value_from_treenode(value_node, 'set_index'),
                collection_index=get_value_from_treenode(value_node, 'collection_index')
            )
        except Value.DoesNotExist:
            value = Value(
                project=project,
                snapshot=snapshot,
                attribute=attribute,
                set_index=get_value_from_treenode(value_node, 'set_index'),
                collection_index=get_value_from_treenode(value_node, 'collection_index')
            )

        value.created = value_node.find('created').text
        value.text = get_value_from_treenode(value_node, 'text')

        try:
            option_uri = value_node['option'].get(get_ns_tag('dc:uri', nsmap))
            value.option = Option.objects.get(uri=option_uri)
        except Option.DoesNotExist:
            value.option = None

        value.save()
    else:
        log.info('Skipping value without Attribute.')
