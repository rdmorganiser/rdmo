from django.urls import re_path

from ..views import ConditionsExportView, ConditionsView

urlpatterns = [
    re_path(r'^$', ConditionsView.as_view(), name='conditions'),
    re_path(r'^export/(?P<format>[a-z]+)/$', ConditionsExportView.as_view(), name='conditions_export'),
]
