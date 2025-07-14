from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import EmailValidator
from django.db import transaction
from django.utils.timezone import now

from .models import Invite, Project

User = get_user_model()


def lookup_or_create_invite(
    project: Project,
    username_or_email: str,
    role: str,
) -> Invite:
    """
    1) Try to find a user by EXACT username.
    2) If found and already a member → ValueError("already_member").
    3) Else, try to find by email.
    4) If still not found:
       - If PROJECT_SEND_INVITE is True and the input *validates* as email → send invite to that email.
       - If PROJECT_SEND_INVITE is False → ValueError("email_invites_disabled").
       - If email format invalid → ValueError("invalid_email").
    5) Finally get_or_create the Invite, refresh if expired, set role & token, return it.
    """
    # 1) try exact username match
    try:
        user = User.objects.get(username=username_or_email)
        email = user.email
    except User.DoesNotExist:
        # 2) didn't match a username—try exact email match
        try:
            user = User.objects.get(email__iexact=username_or_email)
            email = user.email

        except User.DoesNotExist as e:
            # 3) no user at all
            if not settings.PROJECT_SEND_INVITE:
                # inviting by email is disabled site-wide
                raise ValueError("email_invites_disabled") from e
            # Validate it's a real-looking email
            try:
                EmailValidator()(username_or_email)
            except DjangoValidationError as ve:
                raise ValueError("invalid_email") from ve

            user = None
            email = username_or_email

        except User.MultipleObjectsReturned as me:
            # ambiguous email match—fall back the same way
            if not settings.PROJECT_SEND_INVITE:
                raise ValueError("email_invites_disabled") from me
            try:
                EmailValidator()(username_or_email)
            except DjangoValidationError as ve:
                raise ValueError("invalid_email") from ve
            user = None
            email = username_or_email

    except User.MultipleObjectsReturned as um:
        # ambiguous username match—treat as error
        raise ValueError("ambiguous_username") from um

    # 4) if we found a user, make sure they're not already a member
    if user is not None and project.memberships.filter(user=user).exists():
        raise ValueError("already_member")

    # 5) create or refresh the invite
    with transaction.atomic():
        qs = Invite.objects.filter(project=project, user=user, email=email)
        if qs.exists():
            invite = qs.latest('timestamp')
            invite.role = role
            if invite.is_expired:
                invite.timestamp = now()
                invite.make_token()
            invite.save()
            return invite

        invite = Invite(project=project, user=user, email=email, role=role)
        invite.make_token()
        invite.save()
        return invite
