from django.conf.urls import url

from .views import CatalogsView, CatalogExportView

urlpatterns = [
    url(r'^catalogs/(?P<pk>[0-9]+)/export/(?P<format>[a-z]+)/$', CatalogExportView.as_view(), name='questions_catalog_export'),
    url(r'^catalogs/', CatalogsView.as_view(), name='catalogs'),
]
