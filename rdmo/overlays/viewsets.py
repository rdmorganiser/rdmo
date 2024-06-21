from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import Overlay


def check_overlays_enabled():
    if not settings.OVERLAYS:
        raise NotFound("Overlays are disabled")

def get_overlays_for_url(url_name):
    overlays = settings.OVERLAYS.get(url_name)
    if not overlays:
        raise NotFound()
    return overlays

def get_or_create_overlay(user, site, url_name, default_current):
    try:
        overlay = Overlay.objects.get(user=user, site=site, url_name=url_name)
    except Overlay.DoesNotExist:
        overlay = Overlay.objects.create(user=user, site=site, url_name=url_name, current=default_current)
    return overlay


class OverlayViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='(?P<url_name>[-\\w]+)/current')
    def current(self, request, url_name=None):
        check_overlays_enabled()
        overlays = get_overlays_for_url(url_name)
        overlay = get_or_create_overlay(request.user, get_current_site(request), url_name, overlays[0])

        return Response({
            'overlay': overlay.current,
            'last': overlay.current == overlays[-1]
        })

    @action(detail=False, methods=['post'], url_path='(?P<url_name>[-\\w]+)/next')
    def next(self, request, url_name=None):
        check_overlays_enabled()
        overlays = get_overlays_for_url(url_name)
        overlay = get_or_create_overlay(request.user, get_current_site(request), url_name, overlays[0])

        try:
            overlay.current = overlays[overlays.index(overlay.current) + 1]
        except (IndexError, ValueError):
            overlay.current = ''
        overlay.save()

        return Response({
            'overlay': overlay.current,
            'last': overlay.current == overlays[-1]
        })

    @action(detail=False, methods=['post'], url_path='(?P<url_name>[-\\w]+)/dismiss')
    def dismiss(self, request, url_name=None):
        check_overlays_enabled()
        overlay = get_or_create_overlay(request.user, get_current_site(request), url_name, '')
        overlay.current = ''
        overlay.save()

        return Response({'overlay': overlay.current})
