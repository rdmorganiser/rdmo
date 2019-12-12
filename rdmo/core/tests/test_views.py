import pytest
from django.urls import reverse

users = (
    ('editor', 'editor'),
    ('reviewer', 'reviewer'),
    ('user', 'user'),
    ('api', 'api'),
)


@pytest.mark.django_db
def test_home_anonymous(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize("username,password", users)
def test_home_user(client, username, password):
    client.login(username=username, password=password)
    response = client.get(reverse('home'))
    assert response.status_code == 302
    assert response.url == reverse('projects')


@pytest.mark.django_db
def test_i18n_switcher(client):
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
