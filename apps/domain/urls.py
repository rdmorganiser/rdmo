from django.conf.urls import url

from .views import DomainView, DomainExportView

urlpatterns = [
    url(r'^$', DomainView.as_view(), name='domain'),
    url(r'^export/(?P<format>[a-z]+)/$', DomainExportView.as_view(), name='domain_export'),
]
