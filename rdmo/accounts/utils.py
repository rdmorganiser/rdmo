import logging

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from .models import Role
from .settings import GROUPS

log = logging.getLogger(__name__)


def get_full_name(user):
    if user.first_name and user.last_name:
        return f'{user.first_name} {user.last_name}'
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

    database_user = get_user_from_db_or_none(username, email)

    if database_user is None:
        log.info('Deletion of user "%s" failed, get_user_from_db_or_none returned None.', username)
        return False

    if user != database_user:
        log.info('Deletion of user "%s" failed, the user from request (pk=%s) and database (pk=%s) differ.',
                 username, user.pk, database_user.pk)
        return False

    if user.has_usable_password() and password is not None:
        authenticated = authenticate(username=username, password=password)
        if authenticated is None:
            log.info('Deletion of user with usable password "%s" failed, authenticate returned None.', username)
            return False
        try:
            user.delete()
            log.info('Deletion of user with usable password "%s" succeeded.', username)
            return True
        except Exception as e:
            log.error('Deletion of user with usable password "%s" failed, an exception (%s) occured',
                      str(e), username)
            return False
    elif not user.has_usable_password() and password is None:
        try:
            user.delete()
            log.info('Deletion of user without usable password "%s" succeeded.', username)
            return True
        except Exception as e:
            log.error('Deletion of user without usable password "%s" failed, an exception (%s) occured',
                      str(e), username)
            return False
    else:
        log.info('Deletion of user "%s" failed, probably wrong value for password given', username)
        return False


def get_user_from_db_or_none(username: str, email: str):
    try:
        db_user = get_user_model().objects.get(username=username, email=email)
        return db_user
    except ObjectDoesNotExist:
        log.error('Retrieval of user "%s" with email "%s" failed, user does not exist', username, email)
        return None
