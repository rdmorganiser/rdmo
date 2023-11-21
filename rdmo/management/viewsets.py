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
from rdmo.core.xml import convert_elements, flat_xml_to_elements, order_elements, read_xml_file

from .constants import RDMO_MODEL_PATH_MAPPER
from .imports import import_elements

logger = logging.getLogger(__name__)



class MetaViewSet(viewsets.ViewSet):

    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        return Response({k: get_model_field_meta(val) for k, val in RDMO_MODEL_PATH_MAPPER})


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

        # step 2: parse xml
        root = read_xml_file(import_tmpfile_name)
        if root is None:
            logger.info('XML parsing error. Import failed.')
            raise ValidationError({'file': [
                _('The content of the xml file does not consist of well formed data or markup.')
            ]})

        # step 3: create element dicts from xml
        try:
            elements = flat_xml_to_elements(root)
        except KeyError as e:
            logger.info('Import failed with KeyError (%s)' % e)
            raise ValidationError({'file': [_('This is not a valid RDMO XML file.')]}) from e
        except TypeError as e:
            logger.info('Import failed with TypeError (%s)' % e)
            raise ValidationError({'file': [_('This is not a valid RDMO XML file.')]}) from e
        except AttributeError as e:
            logger.info('Import failed with AttributeError (%s)' % e)
            raise ValidationError({'file': [_('This is not a valid RDMO XML file.')]}) from e

        # step 4: convert elements from previous versions
        elements = convert_elements(elements, root.attrib.get('version'))

        # step 5: order the elements and return
        elements = order_elements(elements)

        # step 6: convert elements to a list
        elements = list(elements.values())

        # step 8: import the elements if save=True is set
        imported_elements = import_elements(elements, save=is_truthy(request.POST.get('import')), user=request.user)

        # step 9: return the list of, json-serializable, elements
        return Response(imported_elements)


class ImportViewSet(viewsets.ViewSet):

    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        # step 1: store xml file as tmp file
        try:
            elements = request.data['elements']
        except KeyError as e:
            raise ValidationError({'elements': [_('This field may not be blank.')]}) from e
        except TypeError as e:
            raise ValidationError({'elements': [_('This is not a valid RDMO import JSON.')]}) from e

        # step 3: import the elements
        imported_elements = import_elements(elements, user=request.user)

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
        # need to return obj element for ElementSucces reducer?
        serializer = self.serializer_class(obj, context={'request': request})
        return Response(serializer.data)
