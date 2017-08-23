from rdmo.core.utils import get_ns_tag
from rdmo.domain.models import Attribute
from rdmo.options.models import Option

from .models import Condition


def import_conditions(conditions_node):

    nsmap = conditions_node.nsmap

    for condition_node in conditions_node.iterchildren():
        condition_uri = condition_node[get_ns_tag('dc:uri', nsmap)].text

        try:
            condition = Condition.objects.get(uri=condition_uri)
        except Condition.DoesNotExist:
            condition = Condition()

        condition.uri_prefix = condition_uri.split('/conditions/')[0]
        condition.key = condition_uri.split('/')[-1]
        condition.comment = condition_node[get_ns_tag('dc:comment', nsmap)]
        condition.relation = condition_node['relation']

        try:
            source_uri = condition_node['source'].get(get_ns_tag('dc:uri', nsmap))
            condition.source = Attribute.objects.get(uri=source_uri)
        except (AttributeError, Attribute.DoesNotExist):
            condition.source = None

        try:
            condition.target_text = condition_node['target_text']
        except AttributeError:
            condition.target_text = None

        try:
            option_uid = condition_node['target_option'].get(get_ns_tag('dc:uri', nsmap))
            condition.target_option = Option.objects.get(uri=option_uid)
        except (AttributeError, Option.DoesNotExist):
            condition.target_option = None

        condition.save()
