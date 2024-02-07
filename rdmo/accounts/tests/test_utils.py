import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from rdmo.accounts.models import Role
from rdmo.accounts.utils import delete_user, get_full_name, get_user_from_db_or_none, is_site_manager

normal_users = (
    ('user', 'user', 'user@example.com'),
)

site_managers = (
    ('site', 'site', 'site@example.com'),
)

users = (*normal_users, *site_managers)


@pytest.mark.parametrize('username,password,email', users)
def test_get_full_name(db, username, password, email):
    user = get_user_model().objects.get(username=username, email=email)
    assert get_full_name(user) == user.first_name + ' ' + user.last_name


@pytest.mark.parametrize('username,password,email', users)
def test_get_full_name_returns_username(db, username, password, email):
    user = get_user_model().objects.get(username=username, email=email)
    user.first_name = ''
    user.save()
    assert get_full_name(user) == username


def test_is_site_manager_returns_true_for_superuser(admin_user):
    assert is_site_manager(admin_user) is True


def test_is_site_manager_returns_false_for_not_authenticated_user():
    assert is_site_manager(AnonymousUser()) is False


@pytest.mark.parametrize('username,password,email', site_managers)
def test_is_site_manager_returns_true_for_site_managers(db, client, username, password, email):
    client.login(username=username, password=password)
    user = get_user_model().objects.get(username=username, email=email)
    assert is_site_manager(user) is True


@pytest.mark.parametrize('username,password,email', site_managers)
def test_is_site_manager_returns_false_when_role_doesnotexist_(db, client, username, password, email):
    client.login(username=username, password=password)
    Role.objects.all().delete()
    user = get_user_model().objects.get(username=username, email=email)
    assert is_site_manager(user) is False


@pytest.mark.parametrize('username,password,email', users)
def test_delete_user(db, username, password, email):
    user = get_user_model().objects.get(username=username, email=email)
    assert delete_user(user=user, email=email, password=password) is True


@pytest.mark.parametrize('username,password,email', users)
def test_delete_user_when_user_or_email_is_none(db, username, password, email):
    user = get_user_model().objects.get(username=username, email=email)
    for test_user, test_email in ((user, None), (None, email), (None, None)):
        assert delete_user(user=test_user, email=test_email) is False


@pytest.mark.parametrize('username,password,email', users)
def test_delete_user_when_user_is_not_equal_to_db_user(db, username, password, email):
    user = get_user_model().objects.get(username=username, email=email)
    user.pk += 1
    assert delete_user(user=user, email=email, password=None) is False


@pytest.mark.parametrize('username,password,email', users)
def test_delete_user_when_user_with_usable_password_gives_none_for_password(db, username, password, email):
    user = get_user_model().objects.get(username=username, email=email)
    assert delete_user(user=user, email=email, password=None) is False


@pytest.mark.parametrize('username,password,email', users)
def test_delete_user_when_delete_user_raises_an_exception(db, username, password, email):
    user = get_user_model().objects.get(username=username, email=email)
    def _delete(): raise ValueError
    user.delete = _delete
    assert delete_user(user=user, email=email, password=password) is False


@pytest.mark.parametrize('username,password,email', users)
def test_delete_user_without_usable_password_and_raises_an_exception(db, username, password, email):
    user = get_user_model().objects.get(username=username, email=email)
    user.set_unusable_password()
    def _delete(): raise ValueError
    user.delete = _delete
    assert delete_user(user=user, email=email) is False


@pytest.mark.parametrize('username,password,email', users)
def test_get_user_from_db_or_none_returns_user(db, username, password, email):
    user = get_user_model().objects.get(username=username, email=email)
    assert get_user_from_db_or_none(username, email) == user


@pytest.mark.parametrize('username,password,email', users)
def test_get_user_from_db_or_none_returns_none_when_wrong_input_was_given(db, username, password, email):
    for test_username, test_email in ((username, 'none@example.com'), ('none', email), (None, None)):
        assert get_user_from_db_or_none(test_username, test_email) is None
