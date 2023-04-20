import logging

from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from rdmo.conditions.models import Condition
from rdmo.core.imports import handle_uploaded_file
from rdmo.core.utils import get_model_field_meta
from rdmo.core.xml import (convert_elements, flat_xml_to_elements,
                           order_elements, read_xml_file)
from rdmo.domain.models import Attribute
from rdmo.options.models import Option, OptionSet
from rdmo.questions.models import Catalog, Page, Question, QuestionSet, Section
from rdmo.tasks.models import Task
from rdmo.views.models import View

from .imports import check_permissions, import_elements

logger = logging.getLogger(__name__)


class MetaViewSet(viewsets.ViewSet):

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


class ImportViewSet(viewsets.ViewSet):

    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        return Response({})

    def create(self, request, *args, **kwargs):
        # step 1: store xml file as tmp file
        try:
            uploaded_file = request.FILES['file']
        except KeyError:
            raise ValidationError({'file': [_('This field may not be blank.')]})
        else:
            import_tmpfile_name = handle_uploaded_file(uploaded_file)

        # step 2: parse xml
        root = read_xml_file(import_tmpfile_name)
        if root is None:
            logger.info('XML parsing error. Import failed.')
            raise ValidationError({'file': [_('The content of the xml file does not consist of well formed data or markup.')]})

        # step 3: create element dicts from xml
        try:
            unordered_elements = flat_xml_to_elements(root)
        except KeyError as e:
            logger.info('Import failed with KeyError (%s)' % e)
            raise ValidationError({'file': [_('This is not a valid RDMO XML file.')]})
        except TypeError as e:
            logger.info('Import failed with TypeError (%s)' % e)
            raise ValidationError({'file': [_('This is not a valid RDMO XML file.')]})
        except AttributeError as e:
            logger.info('Import failed with AttributeError (%s)' % e)
            raise ValidationError({'file': [_('This is not a valid RDMO XML file.')]})

        # step 4: check if the user has access to those models
        if not check_permissions(unordered_elements, request.user):
            raise PermissionDenied()

        # step 5: convert elements from previous versions
        convert_elements(unordered_elements, root.attrib.get('version'))

        # step 6: order the elements and return
        ordered_elements = {}
        for uri, element in unordered_elements.items():
            order_elements(ordered_elements, unordered_elements, uri, element)

        elements = ordered_elements.values()

        import_elements(elements)

        return Response(elements)
