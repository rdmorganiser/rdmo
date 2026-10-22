from types import SimpleNamespace

import pytest

from django.contrib.sites.models import Site


@pytest.fixture
def sites(settings):
    Site.objects.clear_cache()

    def activate(domain):
        site = Site.objects.get(domain=domain)
        settings.SITE_ID = site.id
        Site.objects.clear_cache()
        return site

    yield SimpleNamespace(activate=activate)

    Site.objects.clear_cache()
