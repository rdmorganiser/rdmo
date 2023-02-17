import rules
from django.contrib.sites.models import Site

from .utils import is_site_manager as is_site_manager_util


@rules.predicate
def is_site_manager(manager, user):
    if is_site_manager_util(manager):
        current_site = Site.objects.get_current()
        return user.role.member.filter(pk=current_site.pk).exists()
    else:
        return False


rules.add_perm('auth.view_user_object', is_site_manager)
