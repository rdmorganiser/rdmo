import rules

from .models import Role


@rules.predicate
def is_manager_for_user(manager, user):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    try:
        return user.role.member.filter(id__in=manager.role.manager.all()).exists()
    except Role.DoesNotExist:
        return False


rules.add_perm('auth.view_user_object', is_manager_for_user)
