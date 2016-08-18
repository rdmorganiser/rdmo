from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views import *

urlpatterns = [
    url(r'^$', views, name='views'),
    url(_(r'^export/(?P<format>[a-z]+)/$'), views_export, name='views_export'),
]
