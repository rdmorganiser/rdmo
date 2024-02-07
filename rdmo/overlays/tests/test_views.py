import pytest

from django.urls import reverse

from ..models import Overlay

users = (
    ('user', 'user'),
    ('anonymous', None)
)


@pytest.mark.parametrize('username,password', users)
def test_reset_overlays_get(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('reset_overlays')
    response = client.get(url)
    if password:
        assert response.status_code == 200
    else:
        assert response.status_code == 302


@pytest.mark.parametrize('username,password', users)
def test_reset_overlays_post(db, client, username, password):
    client.login(username=username, password=password)

    if password:
        assert Overlay.objects.filter(user__username=username).exists() is True

    url = reverse('reset_overlays')
    response = client.post(url)
    if password:
        assert response.status_code == 302
        assert Overlay.objects.filter(user__username=username).exists() is False
    else:
        assert response.status_code == 302
