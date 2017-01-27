from django.conf.urls import url

from .views import catalogs, catalog_export, questions_catalog_export_xml

urlpatterns = [
    url(r'^catalogs/(?P<catalog_id>[0-9]+)/export/(?P<format>[a-z]+)/$', catalog_export, name='questions_catalog_export'),
    url(r'^export/xml/$', questions_catalog_export_xml, name='questions_catalog_export_xml'),
    url(r'^catalogs/', catalogs, name='catalogs'),
]
