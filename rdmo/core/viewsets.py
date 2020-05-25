from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rdmo.core.permissions import HasModelPermission

from .serializers import SiteSerializer, GroupSerializer


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
