import pytest

from django.contrib.auth import get_user_model

normal_users = (
    ('user', 'user', 'user@example.com'),
)

site_managers = (
    ('site', 'site', 'site@example.com'),
)


@pytest.mark.parametrize('username,password,email', normal_users)
def test_is_site_manager_returns_false_for_normal_users(db, client, username, password, email):
    client.login(username=username, password=password)
    user = get_user_model().objects.get(username=username, email=email)
    assert user.role.is_site_manager is False


@pytest.mark.parametrize('username,password,email', site_managers)
def test_is_site_manager_returns_true_for_site_managers(db, client, username, password, email):
    client.login(username=username, password=password)
    user = get_user_model().objects.get(username=username, email=email)
    assert user.role.is_site_manager is True
