
from django.db import models

from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

# from rdmo.core.constants import VALUE_TYPE_CHOICES
# from rdmo.core.exports import XMLResponse
from rdmo.core.permissions import HasModelPermission
# from rdmo.core.views import ChoicesViewSet
from rdmo.core.viewsets import CopyModelMixin

from rdmo.questions.models import Catalog

from rdmo.questions.utils import get_widget_type_choices

from rdmo.questions.managers import CatalogManager

class CatalogTableViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission, )
    # serializer_class = CatalogSerializer

    # TODO: include a filter for search bar, and include filter for current_site only
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'uri',
        'key',
        'comment'
    )

    def get_queryset(self):
        
        catalogs = Catalog.objects.annotate(
                                    projects_count=models.Count('projects', distinct=True), \
                                    sites_count=models.Count('sites',distinct=True))\
                                    .filter_group(self.request.user) \
                                    .filter_availability(self.request.user)
                                    # .filter_current_site() \
        return catalogs
    