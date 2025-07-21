import logging

from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext_lazy as _

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from rdmo.core.imports import handle_uploaded_file
from rdmo.core.permissions import CanToggleElementCurrentSite
from rdmo.core.utils import get_model_field_meta, is_truthy
from rdmo.core.xml import parse_xml_to_elements

from .constants import RDMO_MODEL_PATH_MAPPER
from .imports import import_elements

logger = logging.getLogger(__name__)



class MetaViewSet(viewsets.ViewSet):

    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        return Response({k: get_model_field_meta(val) for k, val in RDMO_MODEL_PATH_MAPPER.items()})


class UploadViewSet(viewsets.ViewSet):

    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        # step 1: store xml file as tmp file
        try:
            uploaded_file = request.FILES['file']
        except KeyError as e:
            raise ValidationError({'file': [_('This field may not be blank.')]}) from e
        else:
            import_tmpfile_name = handle_uploaded_file(uploaded_file)
        try:
            # step 1.1: initialize parse_xml_to_elements
            # step 2-6: parse xml, validate and convert to
            xml_parsed_elements, errors = parse_xml_to_elements(xml_file=import_tmpfile_name)
        except ValidationError as e:
            logger.info('Import failed with XML parsing errors.')
            raise ValidationError({'file': e}) from e

        # step 7: check if valid
        if errors:
            _str_errors = ", ".join(map(str, errors))
            logger.info('Import failed with XML validation errors. %s', _str_errors)
            raise ValidationError({'file': errors})

        # step 8: import the elements if save=True is set
        imported_elements = import_elements(xml_parsed_elements,
                                            save=is_truthy(request.POST.get('import')),
                                            request=request)

        # step 9: return the list of, json-serializable, elements
        return Response(imported_elements)


class ImportViewSet(viewsets.ViewSet):

    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        # step 1: store xml file as tmp file
        try:
            elements_data = request.data['elements']
            elements = {i['uri']: i for i in elements_data if 'uri' in i}
        except KeyError as e:
            raise ValidationError({'elements': [_('This field may not be blank.')]}) from e
        except TypeError as e:
            raise ValidationError({'elements': [_('This is not a valid RDMO import JSON.')]}) from e

        # step 3: import the elements
        imported_elements = import_elements(elements, request=request)

        # step 4: return the list of elements
        return Response(imported_elements)


class ElementToggleCurrentSiteViewSetMixin:

    @action(detail=True, methods=['put'], url_path="toggle-site", permission_classes=[CanToggleElementCurrentSite])
    def toggle_site(self, request, pk=None):
        obj = self.get_object()
        current_site = get_current_site(request)
        has_current_site = obj.sites.filter(id=current_site.id).exists()
        if has_current_site:
            obj.sites.remove(current_site)
        else:
            obj.sites.add(current_site)
        # need to return obj element for ElementSuccess reducer?
        serializer = self.serializer_class(obj, context={'request': request})
        return Response(serializer.data)
