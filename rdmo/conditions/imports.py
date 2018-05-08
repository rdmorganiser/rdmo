import logging

from django.core.exceptions import ValidationError

from rdmo.core.imports import get_value_from_treenode
from rdmo.domain.models import Attribute
from rdmo.options.models import Option
from rdmo.core.utils import get_ns_map, get_ns_tag, get_uri

from .models import Condition
from .validators import ConditionUniqueKeyValidator

log = logging.getLogger(__name__)


def import_conditions(conditions_node):
    log.info('Importing conditions')
    nsmap = get_ns_map(conditions_node.getroot())

    for condition_node in conditions_node.findall('condition'):
        condition_uri = get_uri(condition_node, nsmap)

        try:
            condition = Condition.objects.get(uri=condition_uri)
        except Condition.DoesNotExist:
            condition = Condition()
            log.info('Condition not in db. Created with uri ' + condition_uri)
        else:
            log.info('Condition does exist. Loaded from uri ' + condition_uri)

        condition.uri_prefix = condition_uri.split('/conditions/')[0]
        condition.key = condition_uri.split('/')[-1]
        condition.comment = get_value_from_treenode(condition_node, get_ns_tag('dc:comment', nsmap))
        condition.relation = get_value_from_treenode(condition_node, 'relation')

        try:
            condition_source = get_value_from_treenode(condition_node, 'source', 'attrib')
            source_uri = str(condition_source[get_ns_tag('dc:uri', nsmap)])
            condition.source = Attribute.objects.get(uri=source_uri)
        except (AttributeError, Attribute.DoesNotExist):
            condition.source = None

        try:
            condition.target_text = get_value_from_treenode(condition_node, 'target_text')
        except AttributeError:
            condition.target_text = None

        try:
            condition_target = get_value_from_treenode(condition_node, 'target_option')
            option_uid = get_value_from_treenode(condition_target, get_ns_tag('dc:uri', nsmap))
            condition.target_option = Option.objects.get(uri=option_uid)
        except (AttributeError, Option.DoesNotExist):
            condition.target_option = None

        try:
            ConditionUniqueKeyValidator(condition).validate()
        except ValidationError:
            log.info('Condition not saving "' + str(condition_uri) + '" due to validation error')
            pass
        else:
            log.info('Condition saving to "' + str(condition_uri) + '"')
            condition.save()
