from django.conf import settings
from django.conf.urls import url
from django.views.decorators.cache import cache_page

from .views import OptionsView, OptionsExportView

urlpatterns = [
    url(r'^$', cache_page(settings.CACHE_TIMEOUT)(OptionsView.as_view()), name='options'),
    url(r'^export/(?P<format>[a-z]+)/$', OptionsExportView.as_view(), name='options_export'),
]
