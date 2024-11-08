import json

from django.contrib.auth.models import User
from django.urls import reverse

from ..models import Membership, Value

urlnames = {
    'copy-set': 'v1-projects:project-value-copy-set',
}

set_value_id = 84
set_values_count = 31

other_project_id = 11


def test_copy(db, client):
    '''
    A set can be copied from a project where the user has permissions.
    '''
    client.login(username='user', password='user')

    user = User.objects.get(username='user')

    set_value = Value.objects.get(id=set_value_id)
    values_count = Value.objects.count()

    # add the user to the project with the set value as well as the other project
    Membership.objects.create(project_id=set_value.project.id, user=user, role='author')
    Membership.objects.create(project_id=other_project_id, user=user, role='author')

    url = reverse(urlnames['copy-set'], args=[other_project_id])
    data = {
        'attribute': set_value.attribute.id,
        'set_prefix': set_value.set_prefix,
        'set_index': 0,
        'text': 'new'
    }
    response = client.post(url, data=json.dumps(dict(**data, copy_set_value=set_value_id)),
                                content_type="application/json")
    assert response.status_code == 201
    assert Value.objects.get(
        project=other_project_id,
        snapshot=None,
        **data
    )
    assert Value.objects.count() == values_count + set_values_count + 1  # one is for set/id


def test_copy_forbidden(db, client):
    '''
    A set cannot be copied from a project where the user has no permissions.
    '''
    client.login(username='user', password='user')

    user = User.objects.get(username='user')

    set_value = Value.objects.get(id=set_value_id)
    values_count = Value.objects.count()

    # add the user only to the other project
    Membership.objects.create(project_id=other_project_id, user=user, role='author')

    url = reverse(urlnames['copy-set'], args=[other_project_id])
    data = {
        'attribute': set_value.attribute.id,
        'set_prefix': set_value.set_prefix,
        'set_index': 0,
        'text': 'new'
    }
    response = client.post(url, data=json.dumps(dict(**data, copy_set_value=set_value_id)),
                                content_type="application/json")
    assert response.status_code == 404
    assert Value.objects.count() == values_count


def test_copy_not_found(db, client):
    '''
    A set cannot be copied when the set value does not exist.
    '''
    client.login(username='user', password='user')

    user = User.objects.get(username='user')

    set_value = Value.objects.get(id=set_value_id)
    values_count = Value.objects.count()

    # add the user only to the other project
    Membership.objects.create(project_id=other_project_id, user=user, role='author')

    url = reverse(urlnames['copy-set'], args=[other_project_id])
    data = {
        'attribute': set_value.attribute.id,
        'set_prefix': set_value.set_prefix,
        'set_index': 0,
        'text': 'new'
    }
    response = client.post(url, data=json.dumps(dict(**data, copy_set_value=10000)),
                                content_type="application/json")
    assert response.status_code == 404
    assert Value.objects.count() == values_count


def test_copy_invalid(db, client):
    '''
    A set cannot be copied when copy_set_value is not an int.
    '''
    client.login(username='user', password='user')

    user = User.objects.get(username='user')

    set_value = Value.objects.get(id=set_value_id)
    values_count = Value.objects.count()

    # add the user only to the other project
    Membership.objects.create(project_id=other_project_id, user=user, role='author')

    url = reverse(urlnames['copy-set'], args=[other_project_id])
    data = {
        'attribute': set_value.attribute.id,
        'set_prefix': set_value.set_prefix,
        'set_index': 0,
        'text': 'new'
    }
    response = client.post(url, data=json.dumps(dict(**data, copy_set_value='wrong')),
                                content_type="application/json")
    assert response.status_code == 404
    assert Value.objects.count() == values_count


def test_copy_missing(db, client):
    '''
    A set cannot be copied when copy_set_value is not provided.
    '''
    client.login(username='user', password='user')

    user = User.objects.get(username='user')

    set_value = Value.objects.get(id=set_value_id)
    values_count = Value.objects.count()

    # add the user only to the other project
    Membership.objects.create(project_id=other_project_id, user=user, role='author')

    url = reverse(urlnames['copy-set'], args=[other_project_id])
    data = {
        'attribute': set_value.attribute.id,
        'set_prefix': set_value.set_prefix,
        'set_index': 0,
        'text': 'new'
    }
    response = client.post(url, data=json.dumps(data),
                                content_type="application/json")
    assert response.status_code == 400
    assert Value.objects.count() == values_count


def test_copy_import(db, client):
    '''
    A set can be copied (imported) into an already existing set.
    '''
    client.login(username='user', password='user')

    user = User.objects.get(username='user')

    copy_set_value = Value.objects.get(id=set_value_id)
    values_count = Value.objects.count()

    # add the user to the project with the set value as well as the other project
    Membership.objects.create(project_id=copy_set_value.project.id, user=user, role='author')
    Membership.objects.create(project_id=other_project_id, user=user, role='author')

    # create a new set
    set_value = Value.objects.create(project_id=other_project_id, attribute=copy_set_value.attribute)

    url = reverse(urlnames['copy-set'], args=[other_project_id])
    data = {
        'id': set_value.id
    }

    response = client.post(url, data=json.dumps(dict(**data, copy_set_value=copy_set_value.id)),
                                content_type="application/json")
    assert response.status_code == 201
    assert Value.objects.count() == values_count + set_values_count + 1  # one is the created set/id value


def test_copy_import_not_found(db, client):
    '''
    A set cannot be imported when the set value does not exist.
    '''
    client.login(username='user', password='user')

    user = User.objects.get(username='user')

    copy_set_value = Value.objects.get(id=set_value_id)
    values_count = Value.objects.count()

    # add the user to the project with the set value as well as the other project
    Membership.objects.create(project_id=copy_set_value.project.id, user=user, role='author')
    Membership.objects.create(project_id=other_project_id, user=user, role='author')

    # create a new set
    set_value = Value.objects.create(project_id=other_project_id, attribute=copy_set_value.attribute)

    url = reverse(urlnames['copy-set'], args=[other_project_id])
    data = {
        'id': set_value.id
    }

    response = client.post(url, data=json.dumps(dict(**data, copy_set_value=10000)),
                                content_type="application/json")
    assert response.status_code == 404
    assert Value.objects.count() == values_count + 1  # one is the created set/id value


def test_copy_import_invalid(db, client):
    '''
    A set cannot be imported when copy_set_value is not an int.
    '''
    client.login(username='user', password='user')

    user = User.objects.get(username='user')

    copy_set_value = Value.objects.get(id=set_value_id)
    values_count = Value.objects.count()

    # add the user to the project with the set value as well as the other project
    Membership.objects.create(project_id=copy_set_value.project.id, user=user, role='author')
    Membership.objects.create(project_id=other_project_id, user=user, role='author')

    # create a new set
    set_value = Value.objects.create(project_id=other_project_id, attribute=copy_set_value.attribute)

    url = reverse(urlnames['copy-set'], args=[other_project_id])
    data = {
        'id': set_value.id
    }

    response = client.post(url, data=json.dumps(dict(**data, copy_set_value='wrong')),
                                content_type="application/json")
    assert response.status_code == 404
    assert Value.objects.count() == values_count + 1  # one is the created set/id value
