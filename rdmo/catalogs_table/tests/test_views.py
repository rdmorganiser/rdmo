
import pytest
from django.urls import reverse

# from rdmo.questions.models import Catalog

users = (
    ('editor', 'editor'),
    ('reviewer', 'reviewer'),
    ('user', 'user'),
    ('api', 'api'),
    ('anonymous', None),
)

status_map = {
    'catalogs_table': {
        'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 302
    },
}

catalog_pk = 1

@pytest.mark.parametrize('username,password', users)
def test_catalogs_table(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('catalogs_table')
    response = client.get(url)
    assert response.status_code == status_map['catalogs_table'][username]


@pytest.mark.parametrize('username,password', users)
def test_table_wrapper(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('table_wrapper')
    response = client.get(url)
    assert response.status_code == status_map['catalogs_table'][username]


@pytest.mark.parametrize('username,password', users)
def test_column_locked_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('column_locked_list', args=(catalog_pk,))
    response = client.get(url)
    assert response.status_code == status_map['catalogs_table'][username]


@pytest.mark.parametrize('username,password', users)
def test_column_available_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('column_available_list', args=(catalog_pk,))
    response = client.get(url)
    assert response.status_code == status_map['catalogs_table'][username]

@pytest.mark.parametrize('username,password', users)
def test_column_sites_list(db, client, username, password):
    client.login(username=username, password=password)

    # url = reverse('column_sites_list', args=(catalog_pk,))
    response = client.get(url)
    assert response.status_code == status_map['catalogs_table'][username]