from django.conf import settings
from django.db import models


class ProjectCurrentSiteManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(project__site__id=settings.SITE_ID)
