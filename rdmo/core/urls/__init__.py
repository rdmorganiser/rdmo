from django.urls import include, path, re_path
from django.views.i18n import JavaScriptCatalog

from rdmo.core.views import i18n_switcher

urlpatterns = [
    path('account/', include('rdmo.accounts.urls')),
    path('conditions/', include('rdmo.conditions.urls')),
    path('domain/', include('rdmo.domain.urls')),
    path('management/', include('rdmo.management.urls')),
    path('options/', include('rdmo.options.urls')),
    path('overlays/', include('rdmo.overlays.urls')),
    path('projects/', include('rdmo.projects.urls')),
    path('questions/', include('rdmo.questions.urls')),
    path('services/', include('rdmo.services.urls')),
    path('tasks/', include('rdmo.tasks.urls')),
    path('views/', include('rdmo.views.urls')),

    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    re_path(r'^i18n/([a-z]{2})/$', i18n_switcher, name='i18n_switcher'),
]
