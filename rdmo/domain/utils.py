from django.db import connection

from .models import Attribute

_SQLITE_ATTRIBUTE_MAP_BATCH_SIZE = 200


def get_attribute_map(attribute_ids):
    # returns the selected attributes and their ancestors
    attribute_ids = sorted({pk for pk in attribute_ids if pk})

    if not attribute_ids:
        return {}

    if connection.vendor != 'sqlite':
        attributes = Attribute.objects.filter(pk__in=attribute_ids)
        return Attribute.objects.get_queryset_ancestors(
            attributes,
            include_self=True,
        ).in_bulk()

    attribute_map = {}

    # django-mptt can create a large OR predicate for fragmented trees.
    # Keep SQLite queries below its expression and parameter limits.
    for offset in range(0, len(attribute_ids), _SQLITE_ATTRIBUTE_MAP_BATCH_SIZE):
        attributes = Attribute.objects.filter(
            pk__in=attribute_ids[offset:offset + _SQLITE_ATTRIBUTE_MAP_BATCH_SIZE]
        )
        attribute_map.update(
            Attribute.objects.get_queryset_ancestors(
                attributes,
                include_self=True,
            ).in_bulk()
        )

    return attribute_map
