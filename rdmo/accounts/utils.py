import logging

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.utils.crypto import get_random_string
from django.utils.text import slugify

from .settings import GROUPS

log = logging.getLogger(__name__)


def get_full_name(user) -> str:
    if user.first_name and user.last_name:
        return f'{user.first_name} {user.last_name}'
    else:
        return user.username


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
            log.error('Deletion of user with usable password "%s" failed, an exception (%s) occurred',
                      str(e), username)
            return False
    elif not user.has_usable_password() and password is None:
        try:
            user.delete()
            log.info('Deletion of user without usable password "%s" succeeded.', username)
            return True
        except Exception as e:
            log.error('Deletion of user without usable password "%s" failed, an exception (%s) occurred',
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


def find_user(user_id=None, username="", email=""):
    username = (username or "").strip()
    email = (email or "").strip().lower()

    if user_id:
        user = get_user_model().objects.filter(pk=user_id).first()
        if user:
            return user

    if username:
        user = get_user_model().objects.filter(username=username).first()
        if user:
            return user

    if email:
        return get_user_model().objects.filter(email__iexact=email).first()

    return None


def make_unique_username(seed: str) -> str:
    base = slugify(seed) or "user"
    user_model = get_user_model()
    for suffix in range(0, 8):
        candidate = base if suffix == 0 else f"{base}_{suffix}"
        if not user_model.objects.filter(username=candidate).exists():
            return candidate
    # fallback
    return f"{base}_{get_random_string(8)}"


def create_user_from_fields(username, email, first_name, last_name):
    username = (username or "").strip()
    email = (email or "").strip().lower()
    first_name = (first_name or "").strip()
    last_name = (last_name or "").strip()

    base = username or (email.split("@")[0] if email else "") or "imported"
    unique = make_unique_username(base)

    user = get_user_model().objects.create_user(
        username=unique,
        email=email,
        first_name=first_name,
        last_name=last_name,
        is_active=True,
    )
    user.set_unusable_password()
    user.save(update_fields=["password"])

    if unique != base:
        log.info("Username '%s' taken, created unique name '%s'.", base, unique)

    return user
