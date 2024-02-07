import re

import pytest

from django.contrib.auth import get_user_model
from django.core import mail
from django.db.models import ObjectDoesNotExist
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from pytest_django.asserts import assertContains, assertNotContains, assertRedirects, assertTemplateUsed, assertURLEqual

from rdmo.accounts.tests.utils import reload_urls

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

boolean_toggle = (True, False)


@pytest.fixture(autouse=True, scope='module')
def reload_urls_at_teardown():
    '''Clear the url cache after the test function.'''
    yield
    reload_urls('accounts')


@pytest.mark.parametrize('profile_update', boolean_toggle)
def test_get_profile_update(db, client, settings, profile_update):
    """
    An authorized GET request to the profile update form returns the form.
    """
    settings.PROFILE_UPDATE = profile_update
    reload_urls('accounts')

    client.login(username='user', password='user')

    url = reverse('profile_update')
    response = client.get(url)
    assert response.status_code == 200
    if settings.PROFILE_UPDATE:
        assertTemplateUsed(response, 'profile/profile_update_form.html')
    else:
        assertTemplateUsed(response, 'profile/profile_update_closed.html')


@pytest.mark.parametrize('profile_update', boolean_toggle)
def test_get_profile_update_redirect(db, client, settings, profile_update):
    """
    An unauthorized GET request to the profile update form gets
    redirected to login.
    """
    settings.PROFILE_UPDATE = profile_update
    reload_urls('accounts')

    client.logout()
    # anynoumous user will be redirected to login in any case
    url = reverse('profile_update')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('account_login') + '?next=' + url


@pytest.mark.parametrize('profile_update', boolean_toggle)
def test_post_profile_update(db, client, settings, profile_update):
    """
    An authorized POST request to the profile update form updates the
    user and redirects to home.
    """
    settings.PROFILE_UPDATE = profile_update
    reload_urls('accounts')

    client.login(username='user', password='user')

    url = reverse('profile_update')
    data = {
        'email': 'test@example.com',
        'first_name': 'Albert',
        'last_name': 'Admin',
        'text': 'text',
        'textarea': 'textarea'
    }
    response = client.post(url, data)

    if settings.PROFILE_UPDATE:
        assert response.status_code == 302
        assert response.url == reverse('home')
    else:
        assert response.status_code == 200


@pytest.mark.parametrize('profile_update', boolean_toggle)
def test_post_profile_update_cancel(db, client, settings, profile_update):
    """
    An authorized POST request to the profile update form updates with
    cancel redirects to home.
    """
    settings.PROFILE_UPDATE = profile_update
    reload_urls('accounts')

    client.login(username='user', password='user')

    url = reverse('profile_update')
    data = {
        'email': 'test@example.com',
        'first_name': 'Albert',
        'last_name': 'Admin',
        'cancel': 'cancel'
    }
    response = client.post(url, data)

    if settings.PROFILE_UPDATE:
        assert response.status_code == 302
        assert response.url == reverse('home')
    else:
        assert response.status_code == 200


@pytest.mark.parametrize('profile_update', boolean_toggle)
def test_post_profile_update_cancel2(db, client, settings, profile_update):
    """
    An authorized POST request to the profile update form updates with
    cancel and the next field redirects to the given url.
    """
    settings.PROFILE_UPDATE = profile_update
    reload_urls('accounts')

    client.login(username='user', password='user')

    url = reverse('profile_update')
    data = {
        'email': 'test@example.com',
        'first_name': 'Albert',
        'last_name': 'Admin',
        'cancel': 'cancel',
        'next': reverse('projects')
    }
    response = client.post(url, data)

    if settings.PROFILE_UPDATE:
        assert response.status_code == 302
        assert response.url == reverse('projects')
    else:
        assert response.status_code == 200


@pytest.mark.parametrize('profile_update', boolean_toggle)
def test_post_profile_update_next(db, client, settings, profile_update):
    """
    An authorized POST request to the profile update form with next field
    updates the user and redirects to the given url.
    """
    settings.PROFILE_UPDATE = profile_update
    reload_urls('accounts')

    client.login(username='user', password='user')

    url = reverse('profile_update')
    data = {
        'email': 'test@example.com',
        'first_name': 'Albert',
        'last_name': 'Admin',
        'text': 'text',
        'textarea': 'textarea',
        'next': reverse('projects')
    }
    response = client.post(url, data)

    if settings.PROFILE_UPDATE:
        assert response.status_code == 302
        assert response.url == reverse('projects')
    else:
        assert response.status_code == 200


@pytest.mark.parametrize('profile_update', boolean_toggle)
def test_post_profile_update_next2(db, client, settings, profile_update):
    """
    An authorized POST request to the profile update form with next
    field set to profile_update updates the user and redirects to home.
    """
    settings.PROFILE_UPDATE = profile_update
    reload_urls('accounts')

    client.login(username='user', password='user')

    url = reverse('profile_update')
    data = {
        'email': 'test@example.com',
        'first_name': 'Albert',
        'last_name': 'Admin',
        'text': 'text',
        'textarea': 'textarea',
        'next': reverse('profile_update')
    }
    response = client.post(url, data)

    if settings.PROFILE_UPDATE:
        assert response.status_code == 302
        assert response.url == reverse('home')
    else:
        assert response.status_code == 200


@pytest.mark.parametrize('account', boolean_toggle)
def test_password_change_get(db, client, settings, account):
    """
    An authorized GET request to the password change form returns the form.
    """
    settings.ACCOUNT = account
    reload_urls('accounts')

    # independent of the setting, the reverse url exists
    client.login(username='user', password='user')

    if settings.ACCOUNT:
        url = reverse('account_change_password')
        response = client.get(url)
        assert response.status_code == 200
    else:
        pytest.raises(NoReverseMatch, reverse, 'account_change_password')


@pytest.mark.parametrize('account', boolean_toggle)
def test_password_change_post(db, client, settings, account):
    """
    An authorized POST request to the password change form updates the
    password and redirects to home.
    """
    settings.ACCOUNT = account
    reload_urls('accounts')

    client.login(username='user', password='user')
    if settings.ACCOUNT:
        url = reverse('account_change_password')
        data = {
            'old_password': 'user',
            'new_password1': 'resu',
            'new_password2': 'resu',
        }
        response = client.post(url, data)
        assert response.status_code == 200
    else:
        pytest.raises(NoReverseMatch, reverse, 'account_change_password')


@pytest.mark.parametrize('account', boolean_toggle)
def test_password_reset_get(db, client, settings, account):
    """
    A GET request to the password reset form returns the form.
    """
    settings.ACCOUNT = account
    reload_urls('accounts')

    if settings.ACCOUNT:
        url = reverse('account_reset_password')
        response = client.get(url)
        assert response.status_code == 200
    else:
        pytest.raises(NoReverseMatch, reverse, 'account_reset_password')


@pytest.mark.parametrize('account', boolean_toggle)
def test_password_reset_post_invalid(db, client, settings, account):
    """
    A POST request to the password reset form with an invalid mail address
    sends no mail.
    """
    settings.ACCOUNT = account
    reload_urls('accounts')

    if settings.ACCOUNT:
        url = reverse('account_reset_password')
        data = {'email': 'wrong@example.com'}
        response = client.post(url, data)
        assert response.status_code == 200
        assert len(mail.outbox) == 0
    else:
        pytest.raises(NoReverseMatch, reverse, 'account_reset_password')


@pytest.mark.urls('rdmo.accounts.urls')
@pytest.mark.parametrize('account', boolean_toggle)
def test_password_reset_post_valid(db, client, settings, account):
    """
    A POST request to the password reset form with an invalid mail address
    sends a mail with a correct link.
    """
    settings.ACCOUNT = account
    reload_urls('accounts')

    if settings.ACCOUNT:
        url = reverse('account_reset_password')
        data = {'email': 'user@example.com'}
        response = client.post(url, data)
        assert response.status_code == 302
        assert response.url == reverse('account_reset_password_done')
        assert len(mail.outbox) == 1

        # get the link from the mail
        complicated_regex = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(complicated_regex, mail.outbox[0].body)
        assert len(urls) == 1

        # get the password_reset page
        response = client.get(urls[0])
        assert response.status_code == 302
        assert response.url == reverse('account_reset_password_from_key', args=['4', 'set-password'])
    else:
        pytest.raises(NoReverseMatch, reverse, 'account_reset_password')


@pytest.mark.parametrize('profile_delete', boolean_toggle)
def test_remove_user_get(db, client, settings, profile_delete):
    settings.PROFILE_DELETE = profile_delete
    reload_urls('accounts')

    client.login(username='user', password='user')
    url = reverse('profile_remove')
    response = client.get(url)

    assert response.status_code == 200
    if settings.PROFILE_DELETE:
        assertTemplateUsed(response, 'profile/profile_remove_form.html')
    else:
        assertTemplateUsed(response, 'profile/profile_remove_closed.html')


@pytest.mark.parametrize('profile_delete', boolean_toggle)
def test_remove_user_post(db, client, settings, profile_delete):
    settings.PROFILE_DELETE = profile_delete
    reload_urls('accounts')

    client.login(username='user', password='user')
    url = reverse('profile_remove')
    data = {
        'email': 'user@example.com',
        'password': 'user',
        'consent': True
    }
    response = client.post(url, data)

    assert response.status_code == 200
    if settings.PROFILE_DELETE:
        assertTemplateUsed(response, 'profile/profile_remove_success.html')
        pytest.raises(ObjectDoesNotExist, get_user_model().objects.get, username='user')
    else:
        assertTemplateUsed(response, 'profile/profile_remove_closed.html')
        assert get_user_model().objects.get(username='user')


@pytest.mark.parametrize('profile_update', boolean_toggle)
def test_remove_user_post_cancelled(db, client, settings, profile_update):
    settings.PROFILE_UPDATE = profile_update
    settings.PROFILE_DELETE = True

    client.login(username='user', password='user')
    url = reverse('profile_remove')
    response = client.post(url, {'cancel': 'cancel'})

    assert response.status_code == 302
    assert get_user_model().objects.filter(username='user').exists()
    if settings.PROFILE_UPDATE:
        assert response.url == '/account'
    else:
        assert response.url == '/'


@pytest.mark.parametrize('profile_delete', boolean_toggle)
def test_remove_user_post_invalid_email(db, client, settings, profile_delete):
    settings.PROFILE_DELETE = profile_delete
    reload_urls('accounts')

    client.login(username='user', password='user')
    url = reverse('profile_remove')
    data = {
        'email': 'invalid',
        'password': 'user',
        'consent': True
    }
    response = client.post(url, data)

    assert response.status_code == 200
    assert get_user_model().objects.get(username='user')
    if settings.PROFILE_DELETE:
        assertTemplateUsed(response, 'profile/profile_remove_failed.html')
    else:
        assertTemplateUsed(response, 'profile/profile_remove_closed.html')


@pytest.mark.parametrize('profile_delete', boolean_toggle)
def test_remove_user_post_invalid_password(db, client, settings, profile_delete):
    settings.PROFILE_DELETE = profile_delete
    reload_urls('accounts')

    client.login(username='user', password='user')
    url = reverse('profile_remove')
    data = {
        'email': 'user@example.com',
        'password': 'invalid',
        'consent': True
    }
    response = client.post(url, data)

    assert response.status_code == 200
    assert get_user_model().objects.get(username='user')
    if settings.PROFILE_DELETE:
        assertTemplateUsed(response, 'profile/profile_remove_failed.html')
    else:
        assertTemplateUsed(response, 'profile/profile_remove_closed.html')


@pytest.mark.parametrize('profile_delete', boolean_toggle)
def test_remove_user_post_invalid_consent(db, client, settings, profile_delete):
    settings.PROFILE_DELETE = profile_delete
    reload_urls('accounts')

    client.login(username='user', password='user')
    url = reverse('profile_remove')
    data = {
        'email': 'user@example.com',
        'password': 'user',
        'consent': False
    }

    response = client.post(url, data)
    assert response.status_code == 200
    if settings.PROFILE_DELETE:
        assertTemplateUsed(response, 'profile/profile_remove_form.html')
        assert response.context['form'].errors['consent'] == ['This field is required.']  # check if consent is required
    else:
        assertTemplateUsed(response, 'profile/profile_remove_closed.html')


@pytest.mark.parametrize('profile_delete', boolean_toggle)
def test_remove_a_user_without_usable_password_post(db, client, settings, profile_delete):
    settings.PROFILE_DELETE = profile_delete
    reload_urls('accounts')

    user = get_user_model().objects.get(username='user', email='user@example.com')
    user.set_unusable_password()
    user.save()

    client.force_login(user=user)  # login without password
    url = reverse('profile_remove')
    data = {
        'email': user.email,
        'consent': True
    }
    response = client.post(url, data)

    assert response.status_code == 200
    if settings.PROFILE_DELETE:
        assertTemplateUsed(response, 'profile/profile_remove_success.html')
        pytest.raises(ObjectDoesNotExist, get_user_model().objects.get, pk=user.pk)
    else:
        assertTemplateUsed(response, 'profile/profile_remove_closed.html')
    client.logout()


@pytest.mark.parametrize('profile_delete', boolean_toggle)
def test_remove_a_user_without_usable_password_post_invalid_email(db, client, settings, profile_delete):
    settings.PROFILE_DELETE = profile_delete
    reload_urls('accounts')

    user = get_user_model().objects.get(username='user', email='user@example.com')
    user.set_unusable_password()
    user.save()

    client.force_login(user=user)  # login without password
    url = reverse('profile_remove')
    data = {
        'email': 'invalid',
        'consent': True
    }
    response = client.post(url, data)

    assert response.status_code == 200
    get_user_model().objects.get(pk=user.pk)
    if settings.PROFILE_DELETE:
        assertTemplateUsed(response, 'profile/profile_remove_failed.html')
    else:
        assertTemplateUsed(response, 'profile/profile_remove_closed.html')
    client.logout()


@pytest.mark.parametrize('profile_delete', boolean_toggle)
def test_remove_a_user_without_usable_password_post_empty_email(db, client, settings, profile_delete):
    settings.PROFILE_DELETE = profile_delete
    reload_urls('accounts')

    user = get_user_model().objects.get(username='user', email='user@example.com')
    user.set_unusable_password()
    user.save()

    client.force_login(user=user)  # login without password
    url = reverse('profile_remove')
    data = {
        'email': '',
        'consent': True
    }
    response = client.post(url, data)

    assert response.status_code == 200
    assert get_user_model().objects.get(pk=user.pk)
    if settings.PROFILE_DELETE:
        assertTemplateUsed(response, 'profile/profile_remove_form.html')
        assert response.context['form'].errors['email'] == ['This field is required.']  # check if email is required
    else:
        assertTemplateUsed(response, 'profile/profile_remove_closed.html')
    client.logout()


@pytest.mark.parametrize('profile_delete', boolean_toggle)
def test_remove_a_user_without_usable_password_post_invalid_consent(db, client, settings, profile_delete):
    settings.PROFILE_DELETE = profile_delete
    reload_urls('accounts')

    user = get_user_model().objects.get(username='user', email='user@example.com')
    user.set_unusable_password()
    user.save()

    client.force_login(user=user)  # login without password
    url = reverse('profile_remove')
    data = {
        'email': user.email,
        'consent': False
    }
    response = client.post(url, data)

    assert response.status_code == 200
    assert get_user_model().objects.get(pk=user.pk)
    if settings.PROFILE_DELETE:
        assertTemplateUsed(response, 'profile/profile_remove_form.html')
        assert response.context['form'].errors['consent'] == ['This field is required.']  # check if consent is required
    else:
        assertTemplateUsed(response, 'profile/profile_remove_closed.html')
    client.logout()


@pytest.mark.parametrize('account_signup', boolean_toggle)
def test_signup(db, client, settings, account_signup):
    settings.ACCOUNT_SIGNUP = account_signup
    reload_urls('accounts')

    url = reverse('account_signup')

    response = client.post(url, {
        'email': 'test@example.com',
        'username': 'test',
        'first_name': 'test',
        'last_name': 'test',
        'password1': 'test',
        'password2': 'test',
    })

    if settings.ACCOUNT_SIGNUP:
        assert response.status_code == 302
        assert response.url == '/'
    else:
        assert response.status_code == 200


@pytest.mark.parametrize('account_signup', boolean_toggle)
def test_signup_next(db, client, settings, account_signup):
    settings.ACCOUNT_SIGNUP = account_signup
    reload_urls('accounts')

    url = reverse('account_signup') + '?next=/about/'
    response = client.post(url, {
        'email': 'test@example.com',
        'username': 'test',
        'first_name': 'test',
        'last_name': 'test',
        'password1': 'test',
        'password2': 'test',
    })

    if settings.ACCOUNT_SIGNUP:
        assert response.status_code == 302
        assert response.url == '/about/'
    else:
        assert response.status_code == 200


@pytest.mark.parametrize('account_terms_of_use', boolean_toggle)
@pytest.mark.parametrize('username,password', users)
def test_terms_of_use(db, client, settings, username, password, account_terms_of_use):
    settings.ACCOUNT_TERMS_OF_USE = account_terms_of_use
    reload_urls('accounts')

    client.login(username=username, password=password)
    if settings.ACCOUNT_TERMS_OF_USE:
        url = reverse('terms_of_use')
        response = client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, 'account/terms_of_use.html')
    else:
        with pytest.raises(NoReverseMatch):
            reverse('terms_of_use')


@pytest.mark.parametrize('account_allow_user_token', boolean_toggle)
def test_token_get_for_user(db, client, settings, account_allow_user_token):
    settings.ACCOUNT_ALLOW_USER_TOKEN = account_allow_user_token
    reload_urls('accounts')

    client.login(username='user', password='user')

    if settings.ACCOUNT_ALLOW_USER_TOKEN:
        url = reverse('account_token')
        response = client.get(url)
        assert response.status_code == 200
    else:
        with pytest.raises(NoReverseMatch):
            reverse('account_token')


@pytest.mark.parametrize('account_allow_user_token', boolean_toggle)
def test_token_get_for_anonymous(db, client, settings, account_allow_user_token):
    settings.ACCOUNT_ALLOW_USER_TOKEN = account_allow_user_token
    reload_urls('accounts')
    client.login(username='anonymous', password=None)

    if settings.ACCOUNT_ALLOW_USER_TOKEN:
        url = reverse('account_token')
        response = client.get(url)
        assert response.status_code == 302
        assert response.url == reverse('account_login') + '?next=' + url
    else:
        with pytest.raises(NoReverseMatch):
            reverse('account_token')


@pytest.mark.parametrize('account_allow_user_token', boolean_toggle)
def test_token_post_for_user(db, client, settings, account_allow_user_token):
    settings.ACCOUNT_ALLOW_USER_TOKEN = account_allow_user_token
    reload_urls('accounts')
    client.login(username='user', password='user')

    if settings.ACCOUNT_ALLOW_USER_TOKEN:
        url = reverse('account_token')
        response = client.post(url)
        assert response.status_code == 200
    else:
        with pytest.raises(NoReverseMatch):
            reverse('account_token')


@pytest.mark.parametrize('account_allow_user_token', boolean_toggle)
def test_token_post_for_anonymous(db, client, settings, account_allow_user_token):
    settings.ACCOUNT_ALLOW_USER_TOKEN = account_allow_user_token
    reload_urls('accounts')
    client.login(username='anonymous', password=None)

    if settings.ACCOUNT_ALLOW_USER_TOKEN:
        url = reverse('account_token')
        response = client.post(url)
        assert response.status_code == 302
        assert response.url == reverse('account_login') + '?next=' + url
    else:
        with pytest.raises(NoReverseMatch):
            reverse('account_token')


@pytest.mark.parametrize('login_form', boolean_toggle)
@pytest.mark.parametrize('username,password', users)
def test_home_login_form(db, client, settings, login_form, username, password):
    settings.LOGIN_FORM = login_form
    reload_urls('accounts')
    # Anonymous user lands on home
    client.login(username='anonymous', password=None)
    url = reverse('home')
    response = client.get(url)

    assert response.status_code == 200
    if settings.LOGIN_FORM:
        assertContains(response, f'<form method="post" action="{reverse("account_login")}"')
    else:
        assertNotContains(response, f'<form method="post" action="{reverse("account_login")}"')


@pytest.mark.parametrize('shibboleth', boolean_toggle)
@pytest.mark.parametrize('username,password', users)
def test_shibboleth_for_home_url(db, client, settings, shibboleth, username, password):
    settings.SHIBBOLETH = shibboleth
    settings.ACCOUNT = False
    reload_urls('accounts')
    # Anonymous user lands on home
    client.login(username='anonymous', password=None)
    url = reverse('home')
    response = client.get(url)

    if settings.SHIBBOLETH:
        # Anyonymous user is redirected to login
        assert response.status_code == 200
        assertContains(response, 'href="' + reverse('shibboleth_login'))


@pytest.mark.parametrize('username,password', users)
def test_shibboleth_login_view(db, client, settings, username, password):
    settings.SHIBBOLETH = True
    settings.SHIBBOLETH_LOGIN_URL = '/shibboleth/login'
    reload_urls('accounts')
    # Anonymous user lands on home
    client.login(username='anonymous', password=None)

    if settings.SHIBBOLETH and settings.SHIBBOLETH_LOGIN_URL:
        url = reverse('shibboleth_login')
        response = client.get(url)

        # Anyonymous user is redirected to login
        assertRedirects(response,
                        settings.SHIBBOLETH_LOGIN_URL + f'?target={response.request["PATH_INFO"]}',
                        target_status_code=404)

        # Redirected user logs in
        if password:
            client.login(username=username, password=password)
            response = client.get(url)
            assertRedirects(response, reverse('projects'))


# @pytest.mark.parametrize('shibboleth', boolean_toggle)
# @pytest.mark.parametrize('shibboleth_login_url', (None, '/shibboleth/login'))
# @pytest.mark.parametrize('username,password', users)
# def test_shibboleth_for_projects_url(db, client, settings, shibboleth, shibboleth_login_url, username, password):
#     settings.SHIBBOLETH = shibboleth
#     settings.SHIBBOLETH_LOGIN_URL = shibboleth_login_url
#     settings.ACCOUNT = False
#     reload_urls('accounts')

#     client.login(username='anonymous', password=None)

#     # Try to access projects
#     url = reverse('projects')
#     response = client.get(url)

#     if settings.SHIBBOLETH and settings.SHIBBOLETH_LOGIN_URL:
#         print(settings.SHIBBOLETH, settings.SHIBBOLETH_LOGIN_URL)
#         # Anyonymous user is redirected to login
#         assert response.status_code == 302

#         assertRedirects(response, reverse('account_login') + '?next=' + reverse('projects'))

#         response = client.get(response.url)

#         # Shibboleth login is shown
#         assert response.status_code == 200
#         assertContains(response, 'href="/account/shibboleth/login/">')

#         # Redirected user logs in
#         client.login(username=username, password=password)
#         response = client.get(response)

#         if password:
#             # Logged in user lands on projects
#             assert response.status_code == 200
#         else:
#             # Anonymous user is redirected to shibboleth login
#             assert response.status_code == 404


@pytest.mark.parametrize('shibboleth', boolean_toggle)
@pytest.mark.parametrize('username,password', users)
def test_shibboleth_logout_username_pattern(db, client, settings, shibboleth, username, password):
    settings.SHIBBOLETH = shibboleth
    settings.SHIBBOLETH_USERNAME_PATTERN = username
    reload_urls('accounts')

    client.login(username=username, password=password)
    if settings.SHIBBOLETH:
        url = reverse('shibboleth_logout')
        response = client.get(url)
        if password is not None:
            assertURLEqual(response.url, reverse('account_logout') + f'?next={settings.SHIBBOLETH_LOGOUT_URL}')
        else:
            assertURLEqual(response.url, reverse('account_logout'))
