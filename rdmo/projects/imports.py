import logging, re

from rdmo.core.utils import get_ns_tag
from rdmo.domain.models import Attribute
from rdmo.options.models import Option
from rdmo.questions.utils import Catalog

from .models import Project, Membership, Snapshot, Value

log = logging.getLogger(__name__)


def get_value_from_xml_node(xml_node, element, what_to_get=None):
    r = None
    try:
        if what_to_get == 'attrib':
            r = str(xml_node.find(element).attrib)
        elif what_to_get == 'tag':
            r = str(xml_node.find(element).tag)
        else:
            r = str(xml_node.find(element).text)
    except Exception as e:
        log.debug('Unable to extract "' + element + '" from "' + str(xml_node) + '". ' + str(e))
        pass
    else:
        try:
            r = r.encode('utf-8', 'ignore')
        except Exception as e:
            log.debug('Unable to decode string to utf-8: ' + str(e))
            pass
    return r


def import_project(project_node, user):
    # TODO: try to extract nsmap, tag seems not to be working
    # nsmap = project_node.tag
    # SHOULD LOOK LIKE THIS:
        # {'dc': 'http://purl.org/dc/elements/1.1/'}

    # project_catalog = get_value_from_xml_node(project_node, 'catalog')
    nsmap = get_value_from_xml_node(project_node, 'catalog')
    project_title = get_value_from_xml_node(project_node, 'title')
    project_created = get_value_from_xml_node(project_node, 'created')
    project_description = get_value_from_xml_node(project_node, 'description')

    try:
        project = Project.objects.get(title=project_title, user=user)
        log.info('Skipping existing project "%s".' % project_title)
        return
    except Project.DoesNotExist:
        log.error(str(Project.DoesNotExist))
        project = Project(title=project_title)

    try:
        # IMPROVEMENT THAT DOES NOT WORK
        # project_catalog = project_node.find("catalog")
        # catalog_uri = project_catalog.get(get_ns_tag('dc:uri', nsmap))
        # MY WORKING VERSION
        catalog_uri = str(re.search(r'[^\']+[^\:]*$', str(nsmap)).group(0)[:-2])
        project.catalog = Catalog.objects.get(uri=catalog_uri)
    except Catalog.DoesNotExist:
        log.error(str(Project.DoesNotExist))
        project.catalog = Catalog.objects.first()

    if project_description:
        project.description = project_description
    else:
        project.description = ''

    project.created = project_created
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
    try:
        snapshot = project.snapshots.get(title=get_value_from_xml_node(snapshot_node, 'title'))
    except Snapshot.DoesNotExist:
        snapshot = Snapshot(project=project, title=get_value_from_xml_node(snapshot_node, 'title'))

    snapshot_description = get_value_from_xml_node(snapshot_node, 'description')
    if snapshot_description:
        snapshot.description = snapshot_description
    else:
        snapshot.description = ''

    snapshot.created = get_value_from_xml_node(snapshot_node, 'created')
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
    log.info("Importing value node: " + str(value_node))
    attribute_uri = get_value_from_xml_node(value_node, 'title')

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
                set_index=get_value_from_xml_node(value_node, 'set_index'),
                collection_index=get_value_from_xml_node(value_node, 'collection_index')
            )
        except Value.DoesNotExist:
            value = Value(
                project=project,
                snapshot=snapshot,
                attribute=attribute,
                set_index=get_value_from_xml_node(value_node, 'set_index'),
                collection_index=get_value_from_xml_node(value_node, 'collection_index')
            )

        value.created = get_value_from_xml_node(value_node, 'created')
        value.text = get_value_from_xml_node(value_node, 'text')

        # NOTE: final use of nsmap
        try:
            option_uri = value_node['option'].get(get_ns_tag('dc:uri', nsmap))
            value.option = Option.objects.get(uri=option_uri)
        except Option.DoesNotExist:
            value.option = None

        value.save()
    else:
        log.info('Skipping value without Attribute.')
