from django.urls import re_path

from ..views import (CatalogCopyView, CatalogExportView, CatalogImportXMLView,
                     CatalogsView)

urlpatterns = [
    re_path(r'^catalogs/(?P<pk>[0-9]+)/export/(?P<format>[a-z]+)/$', CatalogExportView.as_view(), name='questions_catalog_export'),
    re_path(r'^catalogs/copy$', CatalogCopyView.as_view(), name='questions_catalog_copy'),
    re_path(r'^catalogs/import/(?P<format>[a-z]+)/$', CatalogImportXMLView.as_view(), name='questions_catalog_import'),
    re_path(r'^catalogs/', CatalogsView.as_view(), name='catalogs'),
]
