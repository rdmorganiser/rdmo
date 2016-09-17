from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', questions, name='questions'),
    url(r'^catalogs/(?P<catalog_id>[0-9]+)/export/(?P<format>[a-z]+)/$', questions_catalog_export, name='questions_catalog_export'),
]
