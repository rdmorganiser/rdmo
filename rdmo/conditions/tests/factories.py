from rdmo.domain.models import Attribute
from rdmo.options.models import Option

from ..models import Condition

URI_PREFIX = 'https://example.com/condition-prefetch'


def create_conditions(count, uri_path):
    conditions = []
    for index in range(count):
        path = f'{uri_path}-{index:04d}'
        root = Attribute.objects.create(uri_prefix=URI_PREFIX, key=path)
        source = Attribute.objects.create(uri_prefix=URI_PREFIX, key='source', parent=root)
        option = Option.objects.create(uri_prefix=URI_PREFIX, uri_path=path, text_lang1=f'Option {path}')
        conditions.append(Condition.objects.create(
            uri_prefix=URI_PREFIX, uri_path=path, source=source,
            relation=Condition.RELATION_EQUAL, target_option=option
        ))
    return conditions
