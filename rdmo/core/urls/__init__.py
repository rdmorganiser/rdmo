from django.urls import include, path, re_path
from django.views.i18n import JavaScriptCatalog

from rdmo.core.views import i18n_switcher

urlpatterns = [
    path('account/', include('rdmo.accounts.urls')),
    path('management/', include('rdmo.management.urls')),
    path('overlays/', include('rdmo.overlays.urls')),
    path('projects/', include('rdmo.projects.urls')),
    path('services/', include('rdmo.services.urls')),

    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    re_path(r'^i18n/([a-z]{2})/$', i18n_switcher, name='i18n_switcher'),
]
