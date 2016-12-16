from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^catalogs/', catalogs, name='catalogs'),
    url(r'^export/xml/$', questions_catalog_export_xml, name='questions_catalog_export_xml'),
    url(r'^catalogs/(?P<catalog_id>[0-9]+)/export/(?P<format>[a-z]+)/$', catalog_export, name='questions_catalog_export'),

]
