import pytest

import yaml

pytestmark = pytest.mark.django_db

users = (
    'admin',
    'user',
    'anonymous'
)


@pytest.mark.parametrize('username', users)
def test_openapi_schema(db, client, login, settings, username):
    login(username)

    response = client.get('/api/v1/schema/')

    if username in ['admin', 'user']:
        assert response.status_code == 200
        schema = yaml.safe_load(response.content)
        assert schema['openapi'] == '3.0.3'
        assert len(schema['paths']) == 124
    else:
        assert response.status_code == 302


@pytest.mark.parametrize('username', users)
def test_openapi_swagger_ui(client, login, username):
    login(username)

    response = client.get('/api/v1/swagger/')

    if username in ['admin', 'user']:
        assert response.status_code == 200
        assert '<div id="swagger-ui"></div>' in str(response.content)
    else:
        assert response.status_code == 302

@pytest.mark.parametrize('username', users)
def test_openapi_redoc_ui(client, login, username):
    login(username)

    response = client.get('/api/v1/redoc/')

    if username in ['admin', 'user']:
        assert response.status_code == 200
        assert '<redoc spec-url="/api/v1/schema/"></redoc>' in str(response.content)
    else:
        assert response.status_code == 302
