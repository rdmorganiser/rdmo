
from django.contrib.auth.models import AnonymousUser

from rdmo.accounts.utils import is_site_manager, delete_user

def test_is_site_manager_for_superuser(admin_user):
    assert is_site_manager(admin_user) is True

def test_is_site_manager_for_not_authenticated_user():
    assert is_site_manager(AnonymousUser()) is False

def test_delete_user_false():
    assert delete_user(user=None, email=None) is False
