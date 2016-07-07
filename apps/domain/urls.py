from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', domain, name='domain'),
    url(r'^export/$', domain_export, name='domain_export'),
    url(r'^export/(?P<format>[a-z]+)/$', domain_export, name='domain_export'),
]
