
import pytest
from django.urls import reverse


users = (
    ('editor', 'editor'),
    ('reviewer', 'reviewer'),
    ('user', 'user'),
    ('anonymous', None),
)

status_map = {
    'catalogs_table': {
        'editor': 200, 'reviewer': 200, 'user': 403, 'anonymous': 302
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
def test_column_locked_form(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('column_locked_form', args=(catalog_pk,))
    response = client.get(url)
    assert response.status_code == status_map['catalogs_table'][username]


@pytest.mark.parametrize('username,password', users)
def test_column_available_form(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('column_available_form', args=(catalog_pk,))
    response = client.get(url)
    assert response.status_code == status_map['catalogs_table'][username]

@pytest.mark.parametrize('username,password', users)
def test_column_sites_form(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('column_sites_form', args=(catalog_pk,))
    response = client.get(url)
    assert response.status_code == status_map['catalogs_table'][username]

@pytest.mark.parametrize('username,password', users)
def test_column_sites_form(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('column_sites_list', args=(catalog_pk,))
    response = client.get(url)
    assert response.status_code == status_map['catalogs_table'][username]