import pytest

from django.db import connection

from ..models import Attribute
from ..utils import get_attribute_map


@pytest.mark.parametrize('attribute_ids', [[], [None]])
def test_get_attribute_map_empty(db, django_assert_num_queries, attribute_ids):
    with django_assert_num_queries(0):
        assert get_attribute_map(attribute_ids) == {}


def test_get_attribute_map_ancestors(db, django_assert_num_queries):
    root = Attribute.objects.create(key='map-root')
    parent = Attribute.objects.create(key='parent', parent=root)
    first = Attribute.objects.create(key='first', parent=parent)
    second = Attribute.objects.create(key='second', parent=parent)
    Attribute.objects.create(key='unrelated', parent=root)
    Attribute.objects.create(key='other-root')

    with django_assert_num_queries(2):
        attribute_map = get_attribute_map([first.pk, second.pk, first.pk, None])

    assert set(attribute_map) == {root.pk, parent.pk, first.pk, second.pk}
    assert attribute_map[first.pk].parent_id == parent.pk
    assert attribute_map[parent.pk].parent_id == root.pk


def test_get_attribute_map_fragmented_trees(db, django_assert_max_num_queries):
    roots = [Attribute.objects.create(key=f'map-root-{index}') for index in range(201)]
    sources = [Attribute.objects.create(key='source', parent=root) for root in roots]
    expected_ids = {attribute.pk for attribute in roots + sources}

    # sqlite needs two batches
    max_queries = 4 if connection.vendor == 'sqlite' else 2

    with django_assert_max_num_queries(max_queries):
        attribute_map = get_attribute_map(source.pk for source in sources)

    assert set(attribute_map) == expected_ids
