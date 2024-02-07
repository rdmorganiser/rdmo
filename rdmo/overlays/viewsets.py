from django.conf import settings
from django.contrib.sites.models import Site

from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import Overlay


class OverlayViewSet(ViewSet):

    @action(detail=False, methods=['post'], url_path='(?P<url_name>[-\\w]+)/current',
            permission_classes=[IsAuthenticated])
    def current(self, request, url_name=None):
        site = Site.objects.get_current()
        overlays = settings.OVERLAYS.get(url_name)[:]

        if not overlays:
            raise NotFound()

        try:
            overlay = Overlay.objects.get(user=request.user, site=site, url_name=url_name)
        except Overlay.DoesNotExist:
            overlay = Overlay.objects.create(user=request.user, site=site, url_name=url_name, current=overlays[0])

        return Response({
            'overlay': overlay.current,
            'last': overlay.current == overlays[-1]
        })

    @action(detail=False, methods=['post'], url_path='(?P<url_name>[-\\w]+)/next',
            permission_classes=[IsAuthenticated])
    def next(self, request, url_name=None):
        site = Site.objects.get_current()
        overlays = settings.OVERLAYS.get(url_name)[:]
        if not overlays:
            raise NotFound()

        try:
            overlay = Overlay.objects.get(user=request.user, site=site, url_name=url_name)
            try:
                overlay.current = overlays[overlays.index(overlay.current) + 1]
            except (IndexError, ValueError):
                overlay.current = ''
            overlay.save()
        except Overlay.DoesNotExist:
            overlay = Overlay.objects.create(user=request.user, site=site, url_name=url_name, current=overlays[0])

        return Response({
            'overlay': overlay.current,
            'last': overlay.current == overlays[-1]
        })

    @action(detail=False, methods=['post'], url_path='(?P<url_name>[-\\w]+)/dismiss',
            permission_classes=[IsAuthenticated])
    def dismiss(self, request, url_name=None):
        site = Site.objects.get_current()
        overlays = settings.OVERLAYS.get(url_name)[:]
        if not overlays:
            raise NotFound()

        try:
            overlay = Overlay.objects.get(user=request.user, site=site, url_name=url_name)
            overlay.current = ''
            overlay.save()
        except Overlay.DoesNotExist:
            overlay = Overlay.objects.create(user=request.user, site=site, url_name=url_name, current='')

        return Response({'overlay': overlay.current})
