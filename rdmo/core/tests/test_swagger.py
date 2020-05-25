import pytest

users = (
    ('admin', 'admin'),
    ('user', 'user'),
    ('anonymous', None),
)


@pytest.mark.parametrize("username,password", users)
def test_swagger(db, client, username, password):
    client.login(username=username, password=password)

    response = client.get('/api/v1/')

    if password:
        assert response.status_code == 200
    else:
        assert response.status_code == 302
