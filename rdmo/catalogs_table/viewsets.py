import pdb
from django.db import models
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rdmo.core.constants import VALUE_TYPE_CHOICES
from rdmo.core.exports import XMLResponse
from rdmo.core.permissions import HasModelPermission
from rdmo.core.views import ChoicesViewSet
from rdmo.core.viewsets import CopyModelMixin

from rdmo.questions.models import Catalog, Question, QuestionSet, Section
from rdmo.questions.renderers import (CatalogRenderer, QuestionRenderer, QuestionSetRenderer,
                        SectionRenderer)
from rdmo.questions.serializers.export import (CatalogExportSerializer,
                                 QuestionExportSerializer,
                                 QuestionSetExportSerializer,
                                 SectionExportSerializer)
from rdmo.questions.serializers.v1 import (CatalogIndexSerializer, CatalogNestedSerializer,
                             CatalogSerializer, QuestionIndexSerializer,
                             QuestionNestedSerializer, QuestionSerializer,
                             QuestionSetIndexSerializer,
                             QuestionSetNestedSerializer,
                             QuestionSetSerializer, SectionIndexSerializer,
                             SectionNestedSerializer, SectionSerializer)
from rdmo.questions.utils import get_widget_type_choices

from rdmo.questions.managers import CatalogManager


class CatalogTableManager(CatalogManager):

    def order_by_sites(self, reverse=False):
        return sorted(self.get_queryset(), key=lambda x:x.title, reverse=reverse)


class CatalogTableViewSet(CopyModelMixin, ModelViewSet):
    permission_classes = (HasModelPermission, )
    serializer_class = CatalogSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'uri',
        'key',
        'comment'
    )

    def get_queryset(self):
        # print(f'get a.http_method_names: {self.http_method_names}')
        # print(f'self.succes_url {self.success_url}')
        # print(f'self.form_valid {self.form_valid(self.get_form())}')
        print(f'\nget queryset called: {self}\n')
        catalogs = Catalog.objects.annotate(
                                    projects_count=models.Count('projects', distinct=True), \
                                    sites_count=models.Count('sites',distinct=True))\
                                    .filter_current_site() \
                                    .filter_group(self.request.user) \
                                    .filter_availability(self.request.user)
        # pdb.set_trace()
        # Title=models.functions.Coalesce('title_lang1','title_lang2')).exclude(Title__exact='') \\
        # cats2 = catalogs.annotate()
        print(", ".join([i.title for i in catalogs]))
        return catalogs
        # queryset = Catalog.objects.annotate(projects_count=models.Count('projects')) \
        #                           .prefetch_related('sites', 'groups')
    # def oder_by_title(self, reverse=False):
    #         return sorted(self.get_queryset(), key=lambda x:x.title, reverse=reverse)
