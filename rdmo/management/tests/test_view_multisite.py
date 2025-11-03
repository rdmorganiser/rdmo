import pytest

from django.urls import reverse

from rdmo.core.tests.constants import multisite_users
from rdmo.core.tests.utils import multisite_status_map


@pytest.mark.parametrize('username,password', multisite_users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('management')
    response = client.get(url)
    assert response.status_code == multisite_status_map['management'][username]
