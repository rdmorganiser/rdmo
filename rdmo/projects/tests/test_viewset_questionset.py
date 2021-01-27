import pytest
from django.urls import reverse

from rdmo.questions.models import QuestionSet

users = (
    ('owner', 'owner'),
    ('manager', 'manager'),
    ('author', 'author'),
    ('guest', 'guest'),
    ('api', 'api'),
    ('user', 'user'),
    ('site', 'site'),
    ('anonymous', None),
)

urlnames = {
    'list': 'v1-projects:questionset-list',
    'detail': 'v1-projects:questionset-detail',
    'first': 'v1-projects:questionset-first',
    'prev': 'v1-projects:questionset-prev',
    'next': 'v1-projects:questionset-next'
}

questionsets = [1, 2, 78, 79]

catalog_id = 1
catalog_id_wrong = 2


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)

    if password:
        assert response.status_code == 200

        values_list = QuestionSet.objects.order_by_catalog(catalog_id) \
                                         .order_by('id').values_list('id', flat=True)
        assert sorted([item['id'] for item in response.json()]) == list(values_list)
    else:
        assert response.status_code == 401


@pytest.mark.parametrize('username,password', users)
@pytest.mark.parametrize('questionset_id', questionsets)
def test_detail(db, client, username, password, questionset_id):
    client.login(username=username, password=password)

    url = reverse(urlnames['detail'], args=[questionset_id])
    response = client.get(url)

    if password:
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json().get('id') == questionset_id
    else:
        assert response.status_code == 401


# @pytest.mark.parametrize('username,password', users)
# def test_first(db, client, username, password):
#     client.login(username=username, password=password)

#     url = reverse(urlnames['first']) + '?catalog={}'.format(catalog_id)
#     response = client.get(url)

#     if password:
#         assert response.status_code == 200
#         assert response.json().get('id') == QuestionSet.objects.order_by_catalog(catalog_id).first().id
#     else:
#         assert response.status_code == 401


# @pytest.mark.parametrize('username,password', users)
# def test_first_error(db, client, username, password):
#     client.login(username=username, password=password)

#     url = reverse(urlnames['first'])
#     response = client.get(url)

#     if password:
#         assert response.status_code == 404
#     else:
#         assert response.status_code == 401


# @pytest.mark.parametrize('username,password', users)
# @pytest.mark.parametrize('questionset_id', questionsets)
# def test_prev(db, client, username, password, questionset_id):
#     client.login(username=username, password=password)

#     url = reverse(urlnames['prev'], args=[questionset_id])
#     response = client.get(url)

#     if password:
#         if questionset_id == questionsets[0]:
#             assert response.status_code == 404
#         else:
#             assert response.status_code == 200
#             assert response.json().get('id') == questionset_id - 1
#     else:
#         assert response.status_code == 401


# @pytest.mark.parametrize('username,password', users)
# @pytest.mark.parametrize('questionset_id', questionsets)
# def test_next(db, client, username, password, questionset_id):
#     client.login(username=username, password=password)

#     url = reverse(urlnames['next'], args=[questionset_id])
#     response = client.get(url)

#     if password:
#         if questionset_id == questionsets[-1]:
#             assert response.status_code == 404
#         else:
#             assert response.status_code == 200
#             assert response.json().get('id') == questionset_id + 1
#     else:
#         assert response.status_code == 401
