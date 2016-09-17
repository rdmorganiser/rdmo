from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', domain, name='domain'),
    url(r'^export/xml/$', domain_export_xml, name='domain_export_xml'),
    url(r'^export/csv/$', domain_export_csv, name='domain_export_csv'),
    url(r'^export/(?P<format>[a-z]+)/$', domain_export, name='domain_export'),
]
