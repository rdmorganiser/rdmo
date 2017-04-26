from django.contrib.auth.models import Group, Permission

from .settings import GROUPS


def get_full_name(user):
    if user.first_name and user.last_name:
        return '%s %s' % (user.first_name, user.last_name)
    else:
        return user.username


def set_group_permissions():
    for name, permissions in GROUPS:
        group = Group.objects.get(name=name)
        for codename in permissions:
            group.permissions.add(Permission.objects.get(codename=codename))
