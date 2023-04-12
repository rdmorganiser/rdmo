
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from rdmo.accounts.models import Role
from rdmo.accounts.utils import is_site_manager, delete_user, get_user_from_db_or_none

def test_is_site_manager_returns_true_for_superuser(admin_user):
    assert is_site_manager(admin_user) is True

def test_is_site_manager_returns_false_for_not_authenticated_user():
    assert is_site_manager(AnonymousUser()) is False

def test_is_site_manager_returns_true_for_user_site(db, client):
    username = 'site'
    email = 'site@example.com'
    password = 'site'
    client.login(username=username, password=password)
    user = get_user_model().objects.get(username=username, email=email)
    assert is_site_manager(user) is True

def test_is_site_manager_returns_false_when_role_doesnotexist_(db, client):
    username = 'site'
    email = 'site@example.com'
    password = 'site'
    client.login(username=username, password=password)
    Role.objects.all().delete()
    user = get_user_model().objects.get(username=username, email=email)
    assert is_site_manager(user) is False

def test_delete_user_returns_true_for_user(db):
    username = 'user'
    email = 'user@example.com'
    password = 'user'
    user = get_user_model().objects.get(username=username, email=email)
    assert delete_user(user=user, email=email, password=password) is True

def test_delete_user_returns_false_when_user_or_email_is_none(db):
    username = 'user'
    email = 'user@example.com'
    user = get_user_model().objects.get(username=username, email=email)
    for user, email in ((user, None), (None, email), (None, None)):
        assert delete_user(user=user, email=email) is False

def test_delete_user_returns_false_when_user_with_usable_password_gives_none_for_password(db):
    username = 'user'
    email = 'user@example.com'
    password = None
    user = get_user_model().objects.get(username=username, email=email)
    assert delete_user(user=user, email=email, password=password) is False

def test_delete_user_returns_false_when_delete_user_raises_an_exception(db):
    username = 'user'
    email = 'user@example.com'
    password = 'user'
    user = get_user_model().objects.get(username=username, email=email)
    def _delete(): raise ValueError
    user.delete = _delete
    assert delete_user(user=user, email=email, password=password) is False

def test_delete_user_returns_false_when_delete_is_called_for_user_without_usable_password_and_raises_an_exception(db):
    username = 'user'
    email = 'user@example.com'
    password = None
    user = get_user_model().objects.get(username=username, email=email)
    user.set_unusable_password()
    def _delete(): raise ValueError
    user.delete = _delete
    assert delete_user(user=user, email=email, password=password) is False

def test_get_user_from_db_or_none_returns_user(db):
    username = 'user'
    email = 'user@example.com'
    user = get_user_model().objects.get(username=username, email=email)
    assert get_user_from_db_or_none(username, email) == user

def test_get_user_from_db_or_none_returns_none_when_wrong_input_was_given(db):
    username = 'user'
    email = 'user@example.com'
    for username, email in ((username, 'none@example.com'), ('none', email), (None, None)):
        assert get_user_from_db_or_none(username, email) is None
