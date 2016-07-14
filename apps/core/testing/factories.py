from django.contrib.sites.models import Site

from factory.django import DjangoModelFactory

from ..models import *


class SiteFactory(DjangoModelFactory):

    class Meta:
        model = Site

    name = "RDMO"
    domain = "localhost:8000"
