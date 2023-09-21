from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView

from rest_framework_swagger import renderers

from .urls.v1 import urlpatterns


class SwaggerSchemaView(LoginRequiredMixin, APIView):
    renderer_classes = [
        renderers.SwaggerUIRenderer,
    ]

    def get(self, request):
        generator = SchemaGenerator(
            title="RDMO API",
            patterns=urlpatterns,
            url=request.path
        )
        schema = generator.get_schema(request=request)
        return Response(schema)
