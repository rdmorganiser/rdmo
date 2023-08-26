import logging

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from rdmo.projects.models import Membership, Project
from rdmo.questions.models import Catalog
from rdmo.views.models import View

logger = logging.getLogger(__name__)


@receiver(m2m_changed, sender=View.catalogs.through)
def m2m_changed_view_catalog_signal(sender, instance, **kwargs):
    catalogs = instance.catalogs.all()

    if catalogs:
        catalog_candidates = Catalog.objects.exclude(id__in=[catalog.id for catalog in catalogs])

        # Remove catalog candidates for all sites
        projects = Project.objects.filter(catalog__in=catalog_candidates, views=instance)
        for proj in projects:
            proj.views.remove(instance)


@receiver(m2m_changed, sender=View.sites.through)
def m2m_changed_view_sites_signal(sender, instance, **kwargs):
    sites = instance.sites.all()
    catalogs = instance.catalogs.all()

    if sites:
        site_candidates = Site.objects.exclude(id__in=[site.id for site in sites])
        if not catalogs:
            # if no catalogs are selected, update all
            catalogs = Catalog.objects.all()

        # Restrict chosen catalogs for chosen sites
        projects = Project.objects.filter(site__in=site_candidates, catalog__in=catalogs, views=instance)
        for project in projects:
            project.views.remove(instance)


@receiver(m2m_changed, sender=View.groups.through)
def m2m_changed_view_groups_signal(sender, instance, **kwargs):
    groups = instance.groups.all()
    catalogs = instance.catalogs.all()

    if groups:
        users = User.objects.exclude(groups__in=groups)
        memberships = [membership.id for membership in Membership.objects.filter(role='owner', user__in=users)]
        if not catalogs:
            # if no catalogs are selected, update all
            catalogs = Catalog.objects.all()

        # Restrict chosen catalogs for chosen groups
        projects = Project.objects.filter(memberships__in=list(memberships), catalog__in=catalogs, views=instance)
        for project in projects:
            project.views.remove(instance)
