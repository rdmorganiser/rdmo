from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views import *

urlpatterns = [
    url(r'^$', questions, name='questions'),
    url(_(r'^catalogs/(?P<catalog_id>[0-9]+)/pdf/$'), questions_catalog_pdf, name='questions_catalog_pdf'),
]
