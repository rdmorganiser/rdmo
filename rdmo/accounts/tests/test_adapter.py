# import re

# from django.conf import settings
# from django.core import mail
from django.urls import reverse


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
