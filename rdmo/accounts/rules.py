import rules

from rdmo.management.rules import is_an_editor, is_a_reviewer

from .models import Role


@rules.predicate
def is_manager_for_user(user, user_obj):
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


@rules.predicate
def an_editor_or_reviewer_can_see_themselves(user, user_obj):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    try:
        if is_an_editor(user) or is_a_reviewer(user):
            return user == user_obj
        return False
    except Role.DoesNotExist:
        return False


rules.add_perm('auth.view_user_object', is_manager_for_user | an_editor_or_reviewer_can_see_themselves)
