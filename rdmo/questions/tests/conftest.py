import pytest

from django.contrib.sites.models import Site


@pytest.fixture
def site_settings(settings):
    Site.objects.clear_cache()

    def set_site(domain):
        site = Site.objects.get(domain=domain)
        settings.SITE_ID = site.id
        Site.objects.clear_cache()
        return site

    yield set_site

    Site.objects.clear_cache()
