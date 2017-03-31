from django.conf import settings
from django.conf.urls import url
from django.views.decorators.cache import cache_page

from .views import ConditionsView, ConditionsExportView

urlpatterns = [
    url(r'^$', cache_page(settings.CACHE_TIMEOUT)(ConditionsView.as_view()), name='conditions'),
    url(r'^export/(?P<format>[a-z]+)/$', ConditionsExportView.as_view(), name='conditions_export'),
]
