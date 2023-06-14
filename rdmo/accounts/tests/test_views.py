import re

import pytest

from django.contrib.auth import get_user_model
from django.core import mail
from django.db.models import ObjectDoesNotExist
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from pytest_django.asserts import assertTemplateUsed

from rdmo.accounts.tests.utils import reload_app_urlconf_in_testcase

users = (
    ('editor', 'editor'),
    ('reviewer', 'reviewer'),
    ('user', 'user'),
    ('site', 'site'),
    ('api', 'api'),
    ('anonymous', None),
)

boolean_toggle = (True, False)


@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_get_profile_update(db, client, settings, test_setting):
    """
    An authorized GET request to the profile update form returns the form.
    """
    settings.PROFILE_UPDATE = test_setting
    client.login(username='user', password='user')

    url = reverse('profile_update')
    response = client.get(url)
    assert response.status_code == 200
    if settings.PROFILE_UPDATE:
        assertTemplateUsed(response, 'profile/profile_update_form.html')
    else:
        assertTemplateUsed(response, 'profile/profile_update_closed.html')


@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_get_profile_update_redirect(db, client, settings, test_setting):
    """
    An unauthorized GET request to the profile update form gets
    redirected to login.
    """
    settings.PROFILE_UPDATE = test_setting
    client.logout()
    url = reverse('profile_update')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('account_login') + '?next=' + url


@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_post_profile_update(db, client, settings, test_setting):
    """
    An authorized POST request to the profile update form updates the
    user and redirects to home.
    """
    settings.PROFILE_UPDATE = test_setting
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

@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_post_profile_update_cancel(db, client, settings, test_setting):
    """
    An authorized POST request to the profile update form updates with
    cancel redirects to home.
    """
    settings.PROFILE_UPDATE = test_setting
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

@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_post_profile_update_cancel2(db, client, settings, test_setting):
    """
    An authorized POST request to the profile update form updates with
    cancel and the next field redirects to the given url.
    """
    settings.PROFILE_UPDATE = test_setting
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

@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_post_profile_update_next(db, client, settings, test_setting):
    """
    An authorized POST request to the profile update form with next field
    updates the user and redirects to the given url.
    """
    settings.PROFILE_UPDATE = test_setting
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

@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_post_profile_update_next2(db, client, settings, test_setting):
    """
    An authorized POST request to the profile update form with next
    field set to profile_update updates the user and redirects to home.
    """
    settings.PROFILE_UPDATE = test_setting
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

@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_password_change_get(db, client, settings, test_setting):
    """
    An authorized GET request to the password change form returns the form.
    """
    settings.ACCOUNT = test_setting
    # independent of the setting, the reverse url exists
    client.login(username='user', password='user')
    url = reverse('account_change_password')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_password_change_post(db, client, settings, test_setting):
    """
    An authorized POST request to the password change form updates the
    password and redirects to home.
    """
    settings.ACCOUNT = test_setting
    client.login(username='user', password='user')
    url = reverse('account_change_password')
    data = {
        'old_password': 'user',
        'new_password1': 'resu',
        'new_password2': 'resu',
    }
    response = client.post(url, data)
    assert response.status_code == 200


@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_password_reset_get(db, client, settings, test_setting):
    """
    A GET request to the password reset form returns the form.
    """
    settings.ACCOUNT = test_setting

    url = reverse('account_reset_password')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_password_reset_post_invalid(db, client, settings, test_setting):
    """
    A POST request to the password reset form with an invalid mail address
    sends no mail.
    """
    settings.ACCOUNT = test_setting

    url = reverse('account_reset_password')
    data = {'email': 'wrong@example.com'}
    response = client.post(url, data)
    assert response.status_code == 200
    assert len(mail.outbox) == 0


@pytest.mark.urls('rdmo.accounts.urls')
@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_password_reset_post_valid(db, client, settings, test_setting):
    """
    A POST request to the password reset form with an invalid mail address
    sends a mail with a correct link.
    """
    settings.ACCOUNT = test_setting
    reload_app_urlconf_in_testcase('accounts')

    if settings.ACCOUNT:
        url = reverse('account_reset_password')
        data = {'email': 'user@example.com'}
        response = client.post(url, data)
        assert response.status_code == 302
        assert response.url == reverse('account_reset_password_done')
        assert len(mail.outbox) == 1

        # get the link from the mail
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', mail.outbox[0].body)  # complicated regex
        # urls = [i.strip() for i in mail.outbox[0].body.splitlines() if i.strip().startswith('http')]  # simpler alternative
        assert len(urls) == 1

        # get the password_reset page
        response = client.get(urls[0])
        assert response.status_code == 302
        assert response.url == reverse('account_reset_password_from_key', args=['4', 'set-password'])
    else:
        pytest.raises(NoReverseMatch, reverse, 'account_reset_password')


@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_remove_user_get(db, client, settings, test_setting):
    settings.PROFILE_DELETE = test_setting

    client.login(username='user', password='user')
    url = reverse('profile_remove')
    response = client.get(url)

    assert response.status_code == 200
    if settings.PROFILE_DELETE:
        assertTemplateUsed(response, 'profile/profile_remove_form.html')
    else:
        assertTemplateUsed(response, 'profile/profile_remove_closed.html')


@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_remove_user_post(db, client, settings, test_setting):
    settings.PROFILE_DELETE = test_setting

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


@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_remove_user_post_cancelled(db, client, settings, test_setting):
    settings.PROFILE_UPDATE = test_setting
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


@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_remove_user_post_invalid_email(db, client, settings, test_setting):
    settings.PROFILE_DELETE = test_setting

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


@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_remove_user_post_invalid_password(db, client, settings, test_setting):
    settings.PROFILE_DELETE = test_setting

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


@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_remove_user_post_invalid_consent(db, client, settings, test_setting):
    settings.PROFILE_DELETE = test_setting

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


@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_remove_a_user_without_usable_password_post(db, client, settings, test_setting):
    settings.PROFILE_DELETE = test_setting

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


@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_remove_a_user_without_usable_password_post_invalid_email(db, client, settings, test_setting):
    settings.PROFILE_DELETE = test_setting

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


@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_remove_a_user_without_usable_password_post_empty_email(db, client, settings, test_setting):
    settings.PROFILE_DELETE = test_setting

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


@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_remove_a_user_without_usable_password_post_invalid_consent(db, client, settings, test_setting):
    settings.PROFILE_DELETE = test_setting

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


def test_signup(db, client):
    url = reverse('account_signup')
    response = client.post(url, {
        'email': 'test@example.com',
        'username': 'test',
        'first_name': 'test',
        'last_name': 'test',
        'password1': 'test',
        'password2': 'test',
    })

    assert response.status_code == 302
    assert response.url == '/'


def test_signup_next(db, client):
    url = reverse('account_signup') + '?next=/about/'
    response = client.post(url, {
        'email': 'test@example.com',
        'username': 'test',
        'first_name': 'test',
        'last_name': 'test',
        'password1': 'test',
        'password2': 'test',
    })

    assert response.status_code == 302
    assert response.url == '/about/'


@pytest.mark.parametrize('test_setting', boolean_toggle)
@pytest.mark.parametrize('username,password', users)
def test_terms_of_use(db, client, settings, username, password, test_setting):
    settings.ACCOUNT_TERMS_OF_USE = test_setting
    reload_app_urlconf_in_testcase('accounts')
    client.login(username=username, password=password)
    if settings.ACCOUNT_TERMS_OF_USE:
        url = reverse('terms_of_use')
        response = client.get(url)
        assert response.status_code == 200
        assertTemplateUsed('accounts/terms_of_use.html')
    else:
        with pytest.raises(NoReverseMatch):
            reverse('terms_of_use')


@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_token_get_for_user(db, client, settings, test_setting):
    settings.ACCOUNT_ALLOW_USER_TOKEN = test_setting
    reload_app_urlconf_in_testcase('accounts')

    client.login(username='user', password='user')

    if settings.ACCOUNT_ALLOW_USER_TOKEN:
        url = reverse('account_token')
        response = client.get(url)
        assert response.status_code == 200
    else:
        with pytest.raises(NoReverseMatch):
            reverse('account_token')


@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_token_get_for_anonymous(db, client, settings, test_setting):
    settings.ACCOUNT_ALLOW_USER_TOKEN = test_setting
    reload_app_urlconf_in_testcase('accounts')
    client.login(username='anonymous', password=None)

    if settings.ACCOUNT_ALLOW_USER_TOKEN:
        url = reverse('account_token')
        response = client.get(url)
        assert response.status_code == 302
        assert response.url == reverse('account_login') + '?next=' + url
    else:
        with pytest.raises(NoReverseMatch):
            reverse('account_token')


@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_token_post_for_user(db, client, settings, test_setting):
    settings.ACCOUNT_ALLOW_USER_TOKEN = test_setting
    reload_app_urlconf_in_testcase('accounts')
    client.login(username='user', password='user')

    if settings.ACCOUNT_ALLOW_USER_TOKEN:
        url = reverse('account_token')
        response = client.post(url)
        assert response.status_code == 200
    else:
        with pytest.raises(NoReverseMatch):
            reverse('account_token')


@pytest.mark.parametrize('test_setting', boolean_toggle)
def test_token_post_for_anonymous(db, client, settings, test_setting):
    settings.ACCOUNT_ALLOW_USER_TOKEN = test_setting
    reload_app_urlconf_in_testcase('accounts')
    client.login(username='anonymous', password=None)
    # breakpoint()
    if settings.ACCOUNT_ALLOW_USER_TOKEN:
        url = reverse('account_token')
        response = client.post(url)
        assert response.status_code == 302
        assert response.url == reverse('account_login') + '?next=' + url
    else:
        with pytest.raises(NoReverseMatch):
            reverse('account_token')
