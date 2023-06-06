import rules

from .models import Role


@rules.predicate
def is_manager_for_user(user, user_obj):
    ''' checks if the current user is allowed to see another user object '''
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    try:
        if not user.role.manager.exists():
            return False
        return user.role.manager.filter(id__in=user_obj.role.member.all()).exists()
    except Role.DoesNotExist:
        return False


rules.add_perm('auth.view_user_object', is_manager_for_user)
