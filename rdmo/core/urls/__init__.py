from django.urls import include, path, re_path

from rdmo.core.views import i18n_switcher

urlpatterns = [
    path('account/', include('rdmo.accounts.urls')),
    path('conditions/', include('rdmo.conditions.urls')),
    path('domain/', include('rdmo.domain.urls')),
    path('options/', include('rdmo.options.urls')),
    path('projects/', include('rdmo.projects.urls')),
    path('questions/', include('rdmo.questions.urls')),
    path('tasks/', include('rdmo.tasks.urls')),
    path('views/', include('rdmo.views.urls')),

    re_path(r'^i18n/([a-z]{2})/$', i18n_switcher, name='i18n_switcher'),
]
