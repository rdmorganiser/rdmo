from django.conf import settings
from django.conf.urls import url
from django.views.decorators.cache import cache_page

from .views import ViewsView, ViewsExportView

urlpatterns = [
    url(r'^$', cache_page(settings.CACHE_TIMEOUT)(ViewsView.as_view()), name='views'),
    url(r'^export/(?P<format>[a-z]+)/$', ViewsExportView.as_view(), name='views_export'),
]
