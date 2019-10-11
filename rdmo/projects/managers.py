from django.conf import settings
from django.db import models


class CurrentSiteManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(user__role__member=settings.SITE_ID).distinct()


class ProjectCurrentSiteManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(project__user__role__member=settings.SITE_ID).distinct()
