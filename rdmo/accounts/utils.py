import logging

from django.contrib.auth.models import User, Group, Permission

from .settings import GROUPS

log = logging.getLogger(__name__)


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
