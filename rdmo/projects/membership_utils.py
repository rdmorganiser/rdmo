# rdmo/projects/services.py
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import EmailValidator
from django.db.models import Q

from .models import Invite, Membership, Project


def add_or_invite_user(
    project: Project,
    username_or_email: str,
    role: str,
    silent: bool,
    is_site_manager: bool
):
    """
    Attempts to find an existing user by username or email.
    - If found & silent & site-manager → create Membership.
    - Otherwise (or if not found but invites allowed) → create/update Invite.
    Raises ValueError(<code>) on all validation failures:
      * "already_member"
      * "user_not_found"
      * "invalid_email"
      * "silent_invalid"
    """
    User = get_user_model()

    if silent and not is_site_manager:
        raise ValueError("silent_invalid")

    # silent create membership path
    if silent and is_site_manager:
        # *must* be an existing, unique user
        try:
            user = User.objects.get(
                Q(username=username_or_email) |
                Q(email__iexact=username_or_email)
            )
        except (User.DoesNotExist, User.MultipleObjectsReturned) as e:
            # you can not silently add someone who is not a unique, existing user
            raise ValueError("user_not_found") from e

        # can not re-add an existing member
        if project.memberships.filter(user=user).exists():
            raise ValueError("already_member")

        return Membership.objects.create(
            project=project,
            user=user,
            role=role
        )

    # create invite path
    try:
        user = User.objects.get(
            Q(username=username_or_email) |
            Q(email__iexact=username_or_email)
        )
        email = user.email

        if project.memberships.filter(user=user).exists():
            raise ValueError("already_member")

    except (User.DoesNotExist, User.MultipleObjectsReturned) as e:
        # If we are allowed to invite by e-mail
        if settings.PROJECT_SEND_INVITE:
            try:
                EmailValidator()(username_or_email)
            except DjangoValidationError:
                raise ValueError("invalid_email") from e

            user = None
            email = username_or_email
        else:
            raise ValueError("user_not_found") from e

    # Create or update the invite
    invite, _ = Invite.objects.get_or_create(
        project=project,
        user=user,
        email=email
    )
    invite.role = role
    invite.make_token()
    invite.save()
    return invite
