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
        schema_paths = dict(schema['paths'])
        schema_paths.pop('/api/v1/schema/', None)  # ignore self-inclusion for stability
        assert len(schema_paths) == 125
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
