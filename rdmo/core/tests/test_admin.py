import pytest

from django.urls import reverse

sites = (
    (1, 'example.com'),
    (2, 'foo.com'),
    (3, 'bar.com'),
)


@pytest.mark.parametrize('site_id, domain', sites)
def test_admin_sites_site(admin_client, site_id, domain):
    url = reverse('admin:sites_site_changelist') + f'?q={domain}'
    response = admin_client.get(url)

    assert response.status_code == 200
    assert reverse('admin:sites_site_change', args=[site_id]).encode() in response.content
