from django.db.models.signals import post_save
from django.dispatch import receiver

from rdmo.projects.models import Project
from rdmo.views.models import View


@receiver(post_save, sender=Project)
def update_views_on_catalog_change(sender, instance, **kwargs):
    # remove views that are no longer available
    view_candidates = instance.views.exclude(catalogs__in=[instance.catalog]) \
                                    .exclude(catalogs=None)

    for view in view_candidates:
        instance.views.remove(view)

    # add views that are now available
    view_candidates = View.objects.exclude(id__in=[v.id for v in instance.views.all()]) \
                                  .filter_current_site() \
                                  .filter_catalog(instance.catalog)
                                #   .filter_group(self.request.user) \
                                #   .filter_availability(self.request.user).exists()

    for view in view_candidates:
        instance.views.add(view)
