import json

from django.contrib.auth.models import User
from django.urls import reverse

from rdmo.options.models import OptionSet
from rdmo.questions.models import Question

from ..models import Membership, Project, Value

urlnames = {
    'copy-set': 'v1-projects:project-value-copy-set',
}

set_value_id = 84
set_values_count = 33

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


def test_forbidden(db, client):
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


def test_not_found(db, client):
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


def test_invalid(db, client):
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


def test_missing(db, client):
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


def test_empty(db, client):
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
    response = client.post(url, data=json.dumps(dict(**data, copy_set_value='')),
                                content_type="application/json")
    assert response.status_code == 400
    assert Value.objects.count() == values_count


def test_reuse(db, client):
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
    assert Project.objects.get(id=other_project_id).values.count() == set_values_count + 1


def test_reuse_not_found(db, client):
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
    assert Project.objects.get(id=other_project_id).values.count() == 1


def test_reuse_invalid(db, client):
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
    assert Project.objects.get(id=other_project_id).values.count() == 1


def test_reuse_filter(db, client):
    '''
    A set can be copied (imported) into an already existing set.
    '''
    client.login(username='user', password='user')

    user = User.objects.get(username='user')

    set_value = Value.objects.get(id=set_value_id)
    values_count = Value.objects.count()

    # change one question in the catalog
    question = Question.objects.get(id=44)
    question.optionsets.add(OptionSet.objects.get(id=1))

    question = Question.objects.get(id=47)
    question.optionsets.clear()

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
    assert Value.objects.count() == values_count + set_values_count + 1 - 2 # one is for set/id and two are skipped


def test_project_in_post(db, client):
    '''
    A provided project in the post request must not be used.
    '''
    client.login(username='user', password='user')

    user = User.objects.get(username='user')

    set_value = Value.objects.get(id=set_value_id)

    project_id = set_value.project_id

    project_values_count = Value.objects.filter(project_id=project_id).count()
    other_values_count = Value.objects.filter(project_id=other_project_id).count()

    # add the user to the project with the set value and read-only access to the other project
    Membership.objects.create(project_id=set_value.project.id, user=user, role='author')
    Membership.objects.create(project_id=other_project_id, user=user, role='guest')

    url = reverse(urlnames['copy-set'], args=[set_value.project_id])
    data = {
        'attribute': set_value.attribute.id,
        'set_prefix': set_value.set_prefix,
        'set_index': 2,
        'text': 'new',
    }
    response = client.post(url, data=json.dumps(dict(
        **data,
        copy_set_value=set_value_id,
        project=11,  # Project: Other
    )), content_type="application/json")

    assert response.status_code == 201
    assert len(response.json()) == set_values_count + 1

    assert Value.objects.filter(project=project_id, snapshot=None, **data).exists()
    assert not Value.objects.filter(project=other_project_id, snapshot=None, **data).exists()

    assert Value.objects.filter(project_id=project_id).count() == project_values_count + set_values_count + 1
    assert Value.objects.filter(project_id=other_project_id).count() == other_values_count


def test_snapshot_in_post(db, client):
    '''
    A provided snapshot in the post request must not be used.
    '''
    client.login(username='user', password='user')

    user = User.objects.get(username='user')

    set_value = Value.objects.get(id=set_value_id)

    project_id = set_value.project_id
    snapshot_id = set_value.project.snapshots.last().id

    project_values_count = Value.objects.filter(project_id=project_id).count()
    snapshot_values_count = Value.objects.filter(project_id=project_id, snapshot_id=snapshot_id).count()

    # add the user to the project with the set value
    Membership.objects.create(project_id=set_value.project.id, user=user, role='author')

    url = reverse(urlnames['copy-set'], args=[set_value.project_id])
    data = {
        'attribute': set_value.attribute.id,
        'set_prefix': set_value.set_prefix,
        'set_index': 2,
        'text': 'new',
    }
    response = client.post(url, data=json.dumps(dict(
        **data,
        copy_set_value=set_value_id,
        snapshot=snapshot_id,
    )), content_type="application/json")

    assert response.status_code == 201
    assert len(response.json()) == set_values_count + 1

    assert Value.objects.filter(project=project_id, snapshot=None, **data).exists()
    assert not Value.objects.filter(project=project_id, snapshot=snapshot_id, **data).exists()

    assert Value.objects.filter(project_id=project_id).count() == project_values_count + set_values_count + 1
    assert Value.objects.filter(project_id=project_id, snapshot_id=snapshot_id).count() == snapshot_values_count


def test_cross_project(db, client):
    '''
    The value provided in the POST data must not be from another project.
    '''
    client.login(username='user', password='user')
    set_value = Value.objects.get(id=set_value_id)

    user = User.objects.get(username='user')

    project_id = set_value.project_id

    # create a value for Project: Other
    other_set_value = Value.objects.create(
        project_id=other_project_id,
        attribute=set_value.attribute,
        set_prefix=set_value.set_prefix,
        set_index=set_value.set_index,
        text='other'
    )

    values_count = Value.objects.count()

    # add the user to the project with the set value and read-only access to the other project
    Membership.objects.create(project_id=set_value.project.id, user=user, role='author')
    Membership.objects.create(project_id=other_project_id, user=user, role='guest')

    url = reverse(urlnames['copy-set'], args=[project_id])
    data = {
        'id': other_set_value.id,
        'attribute': other_set_value.attribute_id,
        'set_prefix': other_set_value.set_prefix,
        'set_index': other_set_value.set_index,
        'text': 'new',
    }
    response = client.post(url, data=json.dumps(dict(
        **data,
        copy_set_value=set_value_id,
    )), content_type="application/json")

    assert response.status_code == 404
    assert Value.objects.count() == values_count


def test_missing_attribute(db, client):
    '''
    An attribute needs to be provided in the POST data.
    '''
    client.login(username='user', password='user')
    set_value = Value.objects.get(id=set_value_id)

    user = User.objects.get(username='user')

    project_id = set_value.project_id

    project_values_count = Value.objects.filter(project_id=project_id).count()

    # add the user to the project with the set value
    Membership.objects.create(project_id=set_value.project.id, user=user, role='author')

    url = reverse(urlnames['copy-set'], args=[set_value.project_id])
    data = {
        'set_prefix': set_value.set_prefix,
        'set_index': 2,
        'text': 'new',
    }
    response = client.post(url, data=json.dumps(dict(
        **data,
        copy_set_value=set_value_id,
    )), content_type="application/json")

    assert response.status_code == 400

    assert not Value.objects.filter(project=project_id, snapshot=None, **data).exists()
    assert Value.objects.filter(project_id=project_id).count() == project_values_count
