import logging

from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site

from rdmo.questions.models import Catalog
from rdmo.projects.models import Project, Membership

from .models import View

logger = logging.getLogger(__name__)

def m2m_changed_view_catalog_signal(sender, instance, **kwargs):
    catalogs = instance.catalogs.all()

    if catalogs.count() > 0:
        catalog_candidates = Catalog.objects.exclude(id__in=catalogs.values_list('pk')) 

        # Remove catalog candidates for all sites
        projects = Project.objects.filter(catalog__in=catalog_candidates, views=instance)
        for proj in projects:
            proj.views.remove(instance)

def m2m_changed_view_sites_signal(sender, instance, **kwargs):
    sites = instance.sites.all()
    catalogs = instance.catalogs.all()

    if sites.count() > 0:
        site_candidates = Site.objects.exclude(id__in=sites.values_list('pk'))
        if catalogs.count() < 1:
            # if no catalogs are selected, update all
            catalogs = Catalog.objects.all()

        # Restrict chosen catalogs for chosen sites
        projects = Project.objects.filter(site__in=site_candidates, catalog__in=catalogs, views=instance)
        for proj in projects:
            proj.views.remove(instance)

def m2m_changed_view_groups_signal(sender, instance, **kwargs):
    groups = instance.groups.all()
    catalogs = instance.catalogs.all()

    if groups.count() > 0:
        users = User.objects.exclude(groups__in=groups)
        memberships = Membership.objects.filter(role='owner', user__in=users).values_list('pk')
        if catalogs.count() < 1:
            # if no catalogs are selected, update all
            catalogs = Catalog.objects.all()

        # Restrict chosen catalogs for chosen groups
        projects = Project.objects.filter(memberships__in=list(memberships), catalog__in=catalogs, views=instance)
        for proj in projects:
            proj.views.remove(instance)
