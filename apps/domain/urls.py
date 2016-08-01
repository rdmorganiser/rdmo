from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views import *

urlpatterns = [
    url(r'^$', domain, name='domain'),
    url(_(r'^export/(?P<format>[a-z]+)/$'), domain_export, name='domain_export'),
]
