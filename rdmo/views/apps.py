from django.apps import AppConfig
from django.db.models.signals import m2m_changed
from django.utils.translation import gettext_lazy as _


class ViewsConfig(AppConfig):
    name = 'rdmo.views'
    verbose_name = _('Views')

    def ready(self):
        from . import signals
        from .models import View
        m2m_changed.connect(signals.m2m_changed_view_catalog_signal, sender=View.catalogs.through)
        m2m_changed.connect(signals.m2m_changed_view_sites_signal, sender=View.sites.through)
        m2m_changed.connect(signals.m2m_changed_view_groups_signal, sender=View.groups.through)
