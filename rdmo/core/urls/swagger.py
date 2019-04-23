from django.urls import path

from ..swagger import SwaggerSchemaView

urlpatterns = [
    path('', SwaggerSchemaView.as_view()),
]
