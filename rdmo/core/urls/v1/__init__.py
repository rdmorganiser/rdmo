from django.urls import include, path

urlpatterns = [
    path('accounts/', include('rdmo.accounts.urls.v1')),
    path('conditions/', include('rdmo.conditions.urls.v1')),
    path('domain/', include('rdmo.domain.urls.v1')),
    path('management/', include('rdmo.management.urls.v1')),
    path('options/', include('rdmo.options.urls.v1')),
    path('overlays/', include('rdmo.overlays.urls.v1')),
    path('projects/', include('rdmo.projects.urls.v1')),
    path('questions/', include('rdmo.questions.urls.v1')),
    path('tasks/', include('rdmo.tasks.urls.v1')),
    path('views/', include('rdmo.views.urls.v1')),

    path('core/', include('rdmo.core.urls.v1.core')),
]
