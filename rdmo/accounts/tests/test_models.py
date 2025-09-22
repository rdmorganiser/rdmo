import pytest

from django.contrib.auth import get_user_model

normal_users = (
    ('user', 'user', 'user@example.com'),
)

site_editors = (
    ('editor', 'editor', 'editor@example.com'),
    ('example-editor', 'example-editor', 'example-editor@example.com'),
)

site_reviewers = (
    ('reviewer', 'reviewer', 'reviewer@example.com'),
    ('example-reviewer', 'example-reviewer', 'example-reviewer@example.com'),
)



@pytest.mark.parametrize('username,password,email', normal_users)
def test_is_site_editor_returns_false_for_normal_users(db, client, username, password, email):
    client.login(username=username, password=password)
    user = get_user_model().objects.get(username=username, email=email)
    assert user.role.is_editor is False


@pytest.mark.parametrize('username,password,email', site_editors)
def test_is_site_editor_returns_true_for_site_managers(db, client, username, password, email):
    client.login(username=username, password=password)
    user = get_user_model().objects.get(username=username, email=email)
    assert user.role.is_editor is True

@pytest.mark.parametrize('username,password,email', normal_users)
def test_is_site_reviewer_returns_false_for_normal_users(db, client, username, password, email):
    client.login(username=username, password=password)
    user = get_user_model().objects.get(username=username, email=email)
    assert user.role.is_reviewer is False


@pytest.mark.parametrize('username,password,email', site_reviewers)
def test_is_site_reviewer_returns_true_for_site_managers(db, client, username, password, email):
    client.login(username=username, password=password)
    user = get_user_model().objects.get(username=username, email=email)
    assert user.role.is_reviewer is True
