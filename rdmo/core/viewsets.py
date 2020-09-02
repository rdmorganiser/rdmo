from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rdmo.core.permissions import HasModelPermission

from .serializers import GroupSerializer, SiteSerializer


class SettingsViewSet(viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        return Response({
            'default_uri_prefix': settings.DEFAULT_URI_PREFIX
        })


class SitesViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Site.objects.all()
    serializer_class = SiteSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CopyModelMixin:

    @action(detail=True, methods=['PUT'], permission_classes=[HasModelPermission])
    def copy(self, request, pk=None):
        # get the copy relevant data from the request
        uri_prefix = request.data.get('uri_prefix')
        key = request.data.get('key')

        # get the original and the original_serializer
        original = self.get_object()
        original_serializer = self.get_serializer(original)

        # merge the original_serializer with the data from the request and validate
        data = original_serializer.data
        data['uri_prefix'] = uri_prefix
        data['key'] = key
        validation_serializer = self.get_serializer(data=data)
        validation_serializer.is_valid(raise_exception=True)

        # perform the copy on the database
        instance = self.get_object().copy(uri_prefix, key)

        # the rest is similar to CreateModelMixin.create()
        serializer = self.get_serializer(instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
