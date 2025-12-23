import pytest

from django.urls import reverse

from rdmo.config.models import Plugin

users = (
    ('editor', 'editor'),
    ('reviewer', 'reviewer'),
    ('user', 'user'),
    ('api', 'api'),
    ('anonymous', None),
)


@pytest.fixture
def optionset_provider(settings):
    assert 'plugins.optionset_providers.providers.SimpleProvider' in settings.PLUGINS

    plugin = Plugin.objects.get(python_path='plugins.optionset_providers.providers.SimpleProvider')
    plugin.available = True
    plugin.title_lang1 = plugin.title_lang1 or 'Simple OptionSet Provider'
    plugin.url_name = plugin.url_name or 'simple'
    plugin.save()

    return plugin


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, optionset_provider, username, password):
    client.login(username=username, password=password)

    url = reverse('v1-options:provider-list')
    response = client.get(url)

    if password:
        assert response.status_code == 200
        assert {'id': 'simple', 'text': optionset_provider.title} in response.json()
    else:
        assert response.status_code == 401
