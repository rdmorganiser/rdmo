from django.conf.urls import include, url
from django.contrib.auth.mixins import LoginRequiredMixin

from rdmo.accounts.urls import accounts_patterns_api
from rdmo.conditions.urls import conditions_patterns_api
from rdmo.domain.urls import domain_patterns_api
from rdmo.options.urls import options_patterns_api
from rdmo.projects.urls import projects_patterns_api
from rdmo.questions.urls import questions_patterns_api
from rdmo.tasks.urls import tasks_patterns_api
from rdmo.views.urls import views_patterns_api

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers


urlpatterns = [
    url(r'^api/v1/accounts/', include(accounts_patterns_api, namespace='api-v1-accounts')),
    url(r'^api/v1/conditions/', include(conditions_patterns_api, namespace='api-v1-conditions')),
    url(r'^api/v1/domain/', include(domain_patterns_api, namespace='api-v1-domain')),
    url(r'^api/v1/options/', include(options_patterns_api, namespace='api-v1-options')),
    url(r'^api/v1/projects/', include(projects_patterns_api, namespace='api-v1-projects')),
    url(r'^api/v1/questions/', include(questions_patterns_api, namespace='api-v1-questions')),
    url(r'^api/v1/tasks/', include(tasks_patterns_api, namespace='api-v1-tasks')),
    url(r'^api/v1/views/', include(views_patterns_api, namespace='api-v1-views')),
]


class swagger_schema_view(LoginRequiredMixin, APIView):
    permission_classes = [AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer,
    ]

    def get(self, request):
        generator = SchemaGenerator(
            title="RDMO API",
            patterns=urlpatterns,
        )
        schema = generator.get_schema(request=request)
        return Response(schema)
