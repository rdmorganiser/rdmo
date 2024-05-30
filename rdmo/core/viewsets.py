from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.template.loader import get_template

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rdmo.core.permissions import HasModelPermission

from .serializers import GroupSerializer, SiteSerializer


class SettingsViewSet(viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        return Response({
            key.lower(): getattr(settings, key) for key in settings.SETTINGS_API
        })


class SitesViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Site.objects.all()
    serializer_class = SiteSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class TemplatesViewSet(viewsets.GenericViewSet):

    def list(self, request, *args, **kwargs):
        return Response({
            Path(template_path).stem: get_template(template_path).render(request=request).strip()
            for template_path in settings.TEMPLATES_API
        })
