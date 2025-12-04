import pytest

from rdmo.questions.models import Catalog


@pytest.fixture
def clear_sites_from_other_catalogs(settings):
    # arrange, remove sites from the other catalogs
    # for 'list': 'v1-projects:catalog-list'
    # in non-multisite, they should appear
    # however, in a multisite they should not appear
    other_catalogs = Catalog.objects.exclude(sites=settings.SITE_ID)
    assert set(other_catalogs.values_list('id',flat=True)) == {3,4}
    for catalog in other_catalogs:
        catalog.sites.clear()
