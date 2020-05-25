import pytest
from django.urls import reverse

users = (
    ('editor', 'editor'),
    ('reviewer', 'reviewer'),
    ('user', 'user'),
    ('api', 'api'),
)


def test_home_anonymous(db, client):
    response = client.get(reverse('home'))
    assert response.status_code == 200


@pytest.mark.parametrize("username,password", users)
def test_home_user(db, client, username, password):
    client.login(username=username, password=password)
    response = client.get(reverse('home'))
    assert response.status_code == 302
    assert response.url == reverse('projects')


def test_about_anonymous(db, client):
    response = client.get(reverse('about'))
    assert response.status_code == 302


@pytest.mark.parametrize("username,password", users)
def test_about_user(db, client, username, password):
    client.login(username=username, password=password)
    response = client.get(reverse('about'))
    assert response.status_code == 200


def test_i18n_switcher(db, client):
    # get the url to switch to german
    url = reverse('i18n_switcher', args=['de'])

    # switch to german and check if the header is there
    response = client.get(url, HTTP_REFERER='http://testserver/')
    assert response.status_code == 302
    assert 'de' in response['Content-Language']

    # get the url to switch to english
    url = reverse('i18n_switcher', args=['en'])

    # switch to german and check if the header is there
    response = client.get(url)
    assert response.status_code == 302
    assert 'en' in response['Content-Language']
