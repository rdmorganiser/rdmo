from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views import *

urlpatterns = [
    url(r'^$', tasks, name='tasks'),
    url(_(r'^export/(?P<format>[a-z]+)/$'), tasks_export, name='tasks_export'),
]
