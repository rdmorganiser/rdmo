from django.conf import settings

from rest_framework import viewsets
from rest_framework.response import Response


class SettingsViewSet(viewsets.GenericViewSet):

    def list(self, request, *args, **kwargs):
        return Response({
            'default_uri_prefix': settings.DEFAULT_URI_PREFIX
        })
