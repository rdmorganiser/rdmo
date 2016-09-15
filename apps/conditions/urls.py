from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', conditions, name='conditions'),
    url(r'^export/(?P<format>[a-z]+)/$', conditions_export, name='conditions_export'),
]
