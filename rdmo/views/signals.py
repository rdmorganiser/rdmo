import logging

from django.contrib.sites.models import Site

from rdmo.questions.models import Catalog
from rdmo.projects.models.project import Project

from .models import View

logger = logging.getLogger(__name__)

def m2m_changed_view_catalog_signal(sender, instance, action, reverse, pk_set, **kwargs):
    catalogs = instance.catalogs.all()

    if catalogs.count() > 0:
        catalog_candidates = Catalog.objects.exclude(id__in=catalogs.values_list('pk')) 

        # Remove catalog candidates for all sites
        projects = Project.objects.filter(catalog__in=catalog_candidates, views=instance)
        for proj in projects:
            proj.views.remove(instance)

def m2m_changed_view_sites_signal(sender, instance, action, reverse, pk_set, **kwargs):
    sites = instance.sites.all()
    catalogs = instance.catalogs.all()

    if sites.count() > 0:
        site_candidates = Site.objects.exclude(id__in=sites.values_list('pk'))
    
        # Restrict chosen catalogs for chosen sites
        projects = Project.objects.filter(site__in=site_candidates, catalog__in=catalogs, views=instance)
        for proj in projects:
            proj.views.remove(instance)
