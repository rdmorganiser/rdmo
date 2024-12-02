import pytest

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.http import QueryDict

from rdmo.core.tests.utils import compute_checksum

from ..filters import ProjectFilter
from ..models import Project
from ..utils import copy_project, set_context_querystring_with_filter_and_page

GET_queries = [
    'page=2&title=project',
    'page=2',
    'title=project',
    ''
]

@pytest.mark.parametrize('GET_query', GET_queries)
def test_set_context_querystring_with_filter_and_page(GET_query):
    querydict = QueryDict(GET_query)
    filter = ProjectFilter(querydict)
    context = {'filter': filter}
    context = set_context_querystring_with_filter_and_page(context)

    if 'page' in GET_query and 'title' in GET_query:
        assert 'querystring' in context
        assert context['querystring'] == 'title=project'
        querydict_copy = querydict.copy()
        del querydict_copy['page']
        assert context['querystring'] == querydict_copy.urlencode()
    elif 'page' not in GET_query and 'title' in GET_query:
        assert 'querystring' in context
        assert context['querystring'] == 'title=project'
    elif 'page' in GET_query and 'title' not in GET_query:
        assert context.get('querystring', 'not-in-context') == ''
    else:
        assert context.get('querystring', 'not-in-context') == 'not-in-context'


def test_copy_project(db, files):
    project = Project.objects.get(id=1)
    site = Site.objects.get(id=2)
    user = User.objects.get(id=1)
    project_copy = copy_project(project, site, [user])

    # re fetch the original project
    project = Project.objects.get(id=1)

    # check that site, owners, tasks, and views are correct
    assert project_copy.site == site
    assert list(project_copy.owners) == [user]
    assert list(project_copy.user.values('id')) == [{'id': user.id}]
    assert list(project_copy.tasks.values('id')) == list(project.tasks.values('id'))
    assert list(project_copy.views.values('id')) == list(project.views.values('id'))

    # check that no ids are the same
    assert project_copy.id != project.id
    assert not set(project_copy.snapshots.values_list('id')).intersection(set(project.snapshots.values_list('id')))
    assert not set(project_copy.values.values_list('id')).intersection(set(project.values.values_list('id')))

    # check the snapshots
    snapshot_fields = (
        'title',
        'description'
    )
    for snapshot_copy, snapshot in zip(
        project_copy.snapshots.values(*snapshot_fields),
        project.snapshots.values(*snapshot_fields)
    ):
        assert snapshot_copy == snapshot

    # check the values
    value_fields = (
        'attribute',
        'set_prefix',
        'set_collection',
        'set_index',
        'collection_index',
        'text',
        'option',
        'value_type',
        'unit',
        'external_id'
    )
    ordering = (
        'attribute',
        'set_prefix',
        'set_index',
        'collection_index'
    )
    for value_copy, value in zip(
        project_copy.values.filter(snapshot=None).order_by(*ordering),
        project.values.filter(snapshot=None).order_by(*ordering)
    ):
        for field in value_fields:
            assert getattr(value_copy, field) == getattr(value, field), field

        if value_copy.file:
            assert value_copy.file.path != value.file.path
            assert value_copy.file.path == value_copy.file.path.replace(
                f'/projects/{project.id}/values/{value.id}/',
                f'/projects/{project_copy.id}/values/{value_copy.id}/'
            )
            assert value_copy.file.size == value.file.size
            assert compute_checksum(value_copy.file.open('rb').read()) == \
                   compute_checksum(value.file.open('rb').read())
        else:
            assert not value.file

    for snapshot_copy, snapshot in zip(project_copy.snapshots.all(), project.snapshots.all()):
        for value_copy, value in zip(
            project_copy.values.filter(snapshot=snapshot_copy).order_by(*ordering),
            project.values.filter(snapshot=snapshot).order_by(*ordering)
        ):
            for field in value_fields:
                assert getattr(value_copy, field) == getattr(value, field)

            if value_copy.file:
                assert value_copy.file.path != value.file.path
                assert value_copy.file.path == value_copy.file.path.replace(
                    f'/projects/{project.id}/snapshot/{snapshot.id}/values/{value.id}/',
                    f'/projects/{project_copy.id}/snapshot/{snapshot.id}/values/{value_copy.id}/'
                )
                assert value_copy.file.size == value.file.size
                assert compute_checksum(value_copy.file.open('rb').read()) == \
                       compute_checksum(value.file.open('rb').read())
            else:
                assert not value.file
