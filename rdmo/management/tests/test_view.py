import pytest

from django.urls import reverse

users = (
    ('admin', 'admin'),
    ('editor', 'editor'),
    ('reviewer', 'reviewer'),
    ('user', 'user'),
    ('api', 'api'),
    ('anonymous', None)
)

status_map = {
    'management': {
        'admin': 200, 'editor': 200, 'reviewer': 200, 'api': 200, 'user': 403, 'anonymous': 302
    }
}


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse('management')
    response = client.get(url)
    assert response.status_code == status_map['management'][username]
