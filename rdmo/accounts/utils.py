import logging

from django.conf import settings
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType

from .models import Role
from .settings import GROUPS

log = logging.getLogger(__name__)


def get_full_name(user):
    if user.first_name and user.last_name:
        return '%s %s' % (user.first_name, user.last_name)
    else:
        return user.username


def is_site_manager(user):
    if user.is_authenticated:
        if user.is_superuser:
            return True
        else:
            try:
                return user.role.manager.filter(pk=settings.SITE_ID).exists()
            except Role.DoesNotExist:
                return False
    else:
        return False


def set_group_permissions():
    for name, permissions in GROUPS:
        group = Group.objects.get(name=name)
        for app_label, model, codename in permissions:
            content_type = ContentType.objects.get(app_label=app_label, model=model)
            permission = Permission.objects.get(content_type=content_type, codename=codename)
            group.permissions.add(permission)


def delete_user(user, email, password):
    username = user.username

    try:
        database_user = User.objects.get(email=email)
    except User.DoesNotExist:
        log.debug('User with email "%s" requested for deletion does not exist', email)
        return False

    if user == database_user and user.check_password(password):
        try:
            user.delete()
            log.debug('User "%s" deleted', username)
            return True

        except Exception as e:
            log.debug('An exception (%s) occured during user "%s" deletion: ', (str(e), username))
            return False
    else:
        log.debug('Deletion of user "%s" failed because of an invalid password', username)
        return False
