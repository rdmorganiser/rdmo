from django.urls import re_path

from ..views import OptionsExportView, OptionsView

urlpatterns = [
    re_path(r'^$', OptionsView.as_view(), name='options'),
    re_path(r'^export/(?P<format>[a-z]+)/$', OptionsExportView.as_view(), name='options_export'),
]
