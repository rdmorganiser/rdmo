from django.urls import re_path

from ..views import DomainExportView, DomainView

urlpatterns = [
    re_path(r'^$', DomainView.as_view(), name='domain'),
    re_path(r'^export/(?P<format>[a-z]+)/$', DomainExportView.as_view(), name='domain_export')
]
