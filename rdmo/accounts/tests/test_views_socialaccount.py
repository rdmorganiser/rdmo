
from django.urls import reverse
from django.utils.http import urlencode

from .helpers import enable_socialaccount, enable_terms_of_use  # noqa: F401


def test_social_signup(db, client, enable_socialaccount):  # noqa: F811
    # Arrange with enable_socialaccount
    login_url = reverse("dummy_login") + "?" + urlencode({"process": "login"})
    login_response = client.post(login_url)
    assert login_response.status_code == 302
    assert reverse("dummy_authenticate") in login_response.url

    user_data = {
        "id": 99,
        "email": "newuser@example.com",
        "username": "new_user",
        "first_name": "New",
        "last_name": "User",
    }
    auth_response = client.post(login_response.url, user_data)
    assert auth_response.status_code == 302
    assert auth_response.url.startswith(reverse("socialaccount_signup"))

    signup_response = client.post(auth_response.url, user_data)
    assert signup_response.status_code == 302
    assert signup_response.url == reverse('home')

    response = client.get(signup_response.url, follow=True)
    assert response.status_code == 200
    assert (reverse('projects'), 302) in response.redirect_chain


def test_social_signup_with_terms_of_use(
        db, client, enable_terms_of_use, enable_socialaccount  # noqa: F811
    ):
    # Arrange with enable_socialaccount and enable_terms_of_use
    # Arrange: initiate dummy Login
    login_response = client.post(reverse("dummy_login") + "?" + urlencode({"process": "login"}))

    user_data = {
        "id": 199,
        "email": "newuser@example.com",
        "username": "new_user",
        "first_name": "New",
        "last_name": "User",
    }
    # The authentication state is included in the redirected URL
    auth_response = client.post(login_response.url, user_data)
    # Assert, redirected to the signup form (if new user)
    assert auth_response.status_code == 302
    assert auth_response.url == reverse("socialaccount_signup")  # Redirect to signup form

    # Arrange, post to signup without consent
    failed_signup_response = client.post(auth_response.url, user_data)

    # Assert: without consent, signup failed
    content_str = failed_signup_response.content.decode()
    expected_error = 'You need to agree to the terms of use to proceed'
    assert expected_error in content_str, f"Expected error message not found. Response content:\n{content_str}"

    # Arrange: successful post to signup with consent
    user_data['consent'] = True
    signup_response = client.post(auth_response.url, user_data)

    # Assert login was successful and redirected to /projects/
    response = client.get(signup_response.url,follow=True)
    assert response.status_code == 200
    assert (reverse('projects'),302) in response.redirect_chain
