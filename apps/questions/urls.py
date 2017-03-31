from django.conf import settings
from django.conf.urls import url
from django.views.decorators.cache import cache_page

from .views import CatalogsView, CatalogExportView

urlpatterns = [
    url(r'^catalogs/(?P<pk>[0-9]+)/export/(?P<format>[a-z]+)/$', CatalogExportView.as_view(), name='questions_catalog_export'),
    url(r'^catalogs/', cache_page(settings.CACHE_TIMEOUT)(CatalogsView.as_view()), name='catalogs'),
]
