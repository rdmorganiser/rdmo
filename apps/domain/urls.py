from django.conf import settings
from django.conf.urls import url
from django.views.decorators.cache import cache_page

from .views import DomainView, DomainExportView

urlpatterns = [
    url(r'^$', cache_page(settings.CACHE_TIMEOUT)(DomainView.as_view()), name='domain'),
    url(r'^export/(?P<format>[a-z]+)/$', DomainExportView.as_view(), name='domain_export'),
]
