from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rdmo.core.utils import get_model_field_meta

from rdmo.conditions.models import Condition
from rdmo.domain.models import Attribute
from rdmo.options.models import OptionSet, Option
from rdmo.questions.models import Catalog, Section, Page, QuestionSet, Question
from rdmo.tasks.models import Task
from rdmo.views.models import View


class MetaViewSet(viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        return Response({
            'conditions': get_model_field_meta(Condition),
            'attributes': get_model_field_meta(Attribute),
            'optionsets': get_model_field_meta(OptionSet),
            'options': get_model_field_meta(Option),
            'catalogs': get_model_field_meta(Catalog),
            'sections': get_model_field_meta(Section),
            'pages': get_model_field_meta(Page),
            'questionsets': get_model_field_meta(QuestionSet),
            'questions': get_model_field_meta(Question),
            'tasks': get_model_field_meta(Task),
            'views': get_model_field_meta(View)
        })
