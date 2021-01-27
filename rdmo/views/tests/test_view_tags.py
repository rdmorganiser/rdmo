import pytest
from django.template import Context

from rdmo.projects.models import Project
from rdmo.views.templatetags.view_tags import (get_set_value, get_set_values,
                                               get_sets, get_value, get_values)

project_pk = 1


def assertQuerysetEqual(qs1, qs2):
    assert list(qs1.values_list('id')) == list(qs2.values_list('id'))


@pytest.fixture
def context(db):
    return Context({
        'project_id': project_pk,
        'snapshot_id': None
    })


@pytest.fixture
def values(db):
    return Project.objects.get(pk=project_pk).values.filter(snapshot=None).order_by('set_index').order_by('collection_index')


def test_get_value_project_title(context):
    project = Project.objects.get(pk=project_pk)
    assert get_value(context, 'project/title').value == project.title


def test_get_value_project_description(context):
    project = Project.objects.get(pk=project_pk)
    assert get_value(context, 'project/description').value == project.description


def test_get_value_project_created(context):
    project = Project.objects.get(pk=project_pk)
    assert get_value(context, 'project/created').value == project.created


def test_get_value_project_updated(context):
    project = Project.objects.get(pk=project_pk)
    assert get_value(context, 'project/updated').value == project.updated


def test_get_values_uri(context, values):
    uri = 'http://example.com/terms/domain/individual/collection/text'
    assertQuerysetEqual(get_values(context, uri), values.filter(attribute__uri=uri))


def test_get_values(context, values):
    path = 'individual/collection/text'
    assertQuerysetEqual(get_values(context, path), values.filter(attribute__path=path))


def test_get_values_empty(context):
    assert get_values(context, 'individual').exists() is False


def test_get_values_wrong(context):
    assert get_values(context, 'wrong').exists() is False


def test_get_values_set_index(context, values):
    path = 'set/single/text'
    assertQuerysetEqual(get_values(context, path, set_index=1), values.filter(attribute__path=path, set_index=1))


def test_get_values_collection_index(context, values):
    path = 'individual/collection/text'
    assertQuerysetEqual(get_values(context, path, index=1), values.filter(attribute__path=path, collection_index=1))


def test_get_value(context, values):
    path = 'individual/collection/text'
    assert get_value(context, path).id == values.filter(attribute__path=path).first().id


def test_get_set_values(context, values):
    path = 'set/single/text'
    for value_set in get_sets(context, 'set'):
        assertQuerysetEqual(get_set_values(context, value_set, path), values.filter(attribute__path=path, set_index=value_set.set_index))


def test_get_set_value(context, values):
    path = 'set/single/text'
    for value_set in get_sets(context, 'set'):
        assert get_set_value(context, value_set, path).id == values.filter(attribute__path=path, set_index=value_set.set_index).first().id
