from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views import *

urlpatterns = [
    url(r'^$', conditions, name='conditions'),
    url(_(r'^conditions/export/(?P<format>[a-z]+)/$'), conditions_export, name='conditions_export'),
]
