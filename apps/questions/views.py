import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from rest_framework import viewsets, mixins
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from .models import *
from .serializers import *


@login_required()
def questions(request):
    return render(request, 'questions/questions.html', {
        'widget_types': json.dumps([{'id': id, 'text': text} for id, text in Question.WIDGET_TYPE_CHOICES])
    })


class CatalogViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Catalog.objects.all().order_by('pk')

    def get_serializer_class(self):
        if self.action == 'list':
            return CatalogSerializer
        else:
            return NestedCatalogSerializer


class SectionViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class SubsectionViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Subsection.objects.all()
    serializer_class = SubsectionSerializer


class QuestionSetViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = QuestionSet.objects.all()
    serializer_class = QuestionSetSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class WidgetTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )

    serializer_class = WidgetTypeSerializer

    def get_queryset(self):
        return Question.WIDGET_TYPE_CHOICES
