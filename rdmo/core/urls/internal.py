from django.urls import include, path

urlpatterns = [
    path('conditions/', include('rdmo.conditions.urls.internal')),
    path('domain/', include('rdmo.domain.urls.internal')),
    path('options/', include('rdmo.options.urls.internal')),
    path('projects/', include('rdmo.projects.urls.internal')),
    path('questions/', include('rdmo.questions.urls.internal')),
    path('tasks/', include('rdmo.tasks.urls.internal')),
    path('views/', include('rdmo.views.urls.internal')),
]
