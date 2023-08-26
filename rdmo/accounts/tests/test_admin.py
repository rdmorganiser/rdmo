import pytest

from django.urls import reverse

roles = ('member', 'manager', 'editor', 'reviewer')


@pytest.mark.parametrize('role', roles)
def test_admin_accounts_role(admin_client, role):
    url = reverse('admin:accounts_role_changelist') + f'?q={role}'
    response = admin_client.get(url)
    assert response.status_code == 200
