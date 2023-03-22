import logging

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Group, Permission
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


def delete_user(user=None, email=None, password=None):
    if user is None or email is None:
        log.debug('Deletion failed because either User or email is None')
        return False

    username = user.username

    database_user = get_user_model().objects.filter(username=username, email=email)
    if not database_user.exists():
        log.debug('User "%s" requested for deletion does not exist', username)
        return False
    if database_user.count() > 1:
        log.debug('User with email "%s" requested for deletion has multiple user objects', email)
        return False
    database_user = database_user.first()

    if not user == database_user:
        log.debug('Deletion of user "%s" failed because the user from request and database differ.', username)
        return False

    if user.has_usable_password() and password is not None:

        authenticated = authenticate(username=username, password=password)
        if not authenticated:
            log.debug('User with usable password "%s" failed to authenticate, false password.', username)
            return False
        try:
            user.delete()
            log.debug('User "%s" deleted', username)
            return True
        except Exception as e:
            log.debug('An exception (%s) occured during user "%s" deletion: ', (str(e), username))
            return False
    elif not user.has_usable_password() and password is None:
        try:
            user.delete()
            log.debug('User without usable password "%s" deleted', username)
            return True
        except Exception as e:
            log.debug('An exception (%s) occured during user "%s" deletion: ', (str(e), username))
            return False
    else:
        log.debug('Failed to delete user "%s", wrong value for password.', username)
        return False
