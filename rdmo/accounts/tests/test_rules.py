import pytest

from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

from ..rules import is_manager_for_user, an_editor_or_reviewer_can_see_themselves


users = (
    ('editor', 'editor'),
    ('reviewer', 'reviewer'),
    ('user', 'user'),
    ('site', 'site'),
    ('api', 'api'),
    ('anonymous', None),
)

other_site_users = (
    'foo-user',
    'foo-manager',
    'foo-editor',
    'foo-reviewer',
    'bar-user',
    'bar-manager',
    'bar-editor',
    'bar-reviewer',
)

users += tuple(zip(other_site_users, other_site_users))  # add (other site users and passwords)


def test_rules_is_manager_for_user_fails_when_not_authenticated(db):
    """
    An unauthorized user is not a manager for any user.
    """
    user = AnonymousUser()
    user_obj = get_user_model().objects.get(username='user')
    assert not is_manager_for_user(user, user_obj)


@pytest.mark.parametrize('username,password', users)
def test_rules_is_manager_for_user_fails_because_user_has_no_role(db, client, username, password):
    """
    An authorized user that has no role is not a manager for any user.
    """

    user, _created = get_user_model().objects.get_or_create(username=username)
    client.force_login(user)
    user.role = None
    user_obj = get_user_model().objects.first()

    assert not is_manager_for_user(user, user_obj)


@pytest.mark.parametrize('username,password', users)
def test_rules_is_manager_for_user_by_superuser(admin_user, db, username, password):
    """
    A superuser is a manager for any user.
    """
    user_obj, _created = get_user_model().objects.get_or_create(username=username)
    assert is_manager_for_user(admin_user, user_obj)


def test_rules_an_editor_or_reviewer_can_see_themselves_fails_when_not_authenticated(db):
    """
    An unauthorized user is not a manager for any user.
    """
    user = AnonymousUser()
    user_obj = get_user_model().objects.get(username='user')
    assert not an_editor_or_reviewer_can_see_themselves(user, user_obj)


@pytest.mark.parametrize('username,password', users)
def test_rules_an_editor_or_reviewer_can_see_themselves_fails_because_user_has_no_role(db, client, username, password):
    """
    An authorized user that has no role is not a manager for any user.
    """

    user, _created = get_user_model().objects.get_or_create(username=username)
    client.force_login(user)
    user.role = None
    user_obj = get_user_model().objects.first()

    assert not an_editor_or_reviewer_can_see_themselves(user, user_obj)


@pytest.mark.parametrize('username,password', users)
def test_rules_an_editor_or_reviewer_can_see_themselves_fails_because_user_is_not_an_editor_or_reviewer(
    db, client, username, password):
    """
    An authorized user that has no role is not a manager for any user.
    """

    user, _created = get_user_model().objects.get_or_create(username=username)
    
    for user_obj in get_user_model().objects.all():
        if user.is_superuser:
            assert an_editor_or_reviewer_can_see_themselves(user, user_obj) == True
            return

        if user.role.editor.exists() or user.role.reviewer.exists():
            if user == user_obj:
                assert an_editor_or_reviewer_can_see_themselves(user, user_obj) == True
                return
            assert not an_editor_or_reviewer_can_see_themselves(user, user_obj)
            return
        assert not an_editor_or_reviewer_can_see_themselves(user, user_obj)


@pytest.mark.parametrize('username,password', users)
def test_rules_an_editor_or_reviewer_can_see_themselves_is_true_for_superuser(admin_user, db, username, password):
    """
    A superuser is a manager for any user.
    """
    user_obj, _created = get_user_model().objects.get_or_create(username=username)
    assert an_editor_or_reviewer_can_see_themselves(admin_user, user_obj)
