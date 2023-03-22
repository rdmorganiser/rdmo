
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from rdmo.accounts.utils import is_site_manager, delete_user, get_user_from_db_or_none

def test_is_site_manager_for_superuser(admin_user):
    assert is_site_manager(admin_user) is True

def test_is_site_manager_for_not_authenticated_user():
    assert is_site_manager(AnonymousUser()) is False

def test_delete_user_returns_false_user_or_email_is_none():
    assert delete_user(user=None, email=None) is False

def test_delete_user_false_user_with_usable_gives_none_for_password(db, client, settings):
    username = 'user'
    email = 'user@example.com'
    password = None
    db_user = get_user_model().objects.get(username=username, email=email)
    assert delete_user(user=db_user, email=email, password=password) is False

def test_delete_user_false_user_with_usable_password_delete_raises_exception(db, client, settings):
    username = 'user'
    email = 'user@example.com'
    password = 'user'
    db_user = get_user_model().objects.get(username=username, email=email)
    def _delete(): raise ValueError
    db_user.delete = _delete
    assert delete_user(user=db_user, email=email, password=password) is False

def test_delete_user_false_user_without_usable_password_delete_raises_exception(db, client, settings):
    username = 'user'
    email = 'user@example.com'
    password = None
    db_user = get_user_model().objects.get(username=username, email=email)
    db_user.set_unusable_password()
    def _delete(): raise ValueError
    db_user.delete = _delete
    assert delete_user(user=db_user, email=email, password=password) is False

def test_get_user_from_db_or_none_returns_user(db, client, settings):
    username = 'user'
    email = 'user@example.com'
    db_user = get_user_model().objects.get(username=username, email=email)
    assert get_user_from_db_or_none(username, email) == db_user

def test_get_user_from_db_or_none_returns_none(db, client, settings):
    username = None
    email = None
    assert get_user_from_db_or_none(username, email) is None
