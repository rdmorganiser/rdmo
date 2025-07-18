from __future__ import annotations

import dataclasses
from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser

User = get_user_model()


def replace_uri_in_template_string(
    template: str, source_uri: str, target_uri: str
) -> str:
    replacements = [
        (f"'{source_uri}'", f"'{target_uri}'"),
        (f'"{source_uri}"', f'"{target_uri}"'),
    ]
    for pattern, replacement in replacements:
        template = template.replace(pattern, replacement)
    return template


def get_cli_user(spec=None):
    """
    Resolve *spec* to a real User instance (or AnonymousUser if nothing fits).

    * ``None``          → first superuser (fallback: AnonymousUser)
    * ``"42"``          → by primary key
    * ``"alice"``       → by username
    """

    if spec is None:
        return User.objects.filter(is_superuser=True).first() or AnonymousUser()

    if spec.isdigit():
        return User.objects.filter(pk=int(spec)).first() or AnonymousUser()

    return User.objects.filter(username=spec).first() or AnonymousUser()


@dataclasses.dataclass
class FakeRequest:
    """
    Minimal stand-in so legacy import plugins can call ``self.request.user``
    and ``self.request.session`` while running inside a management command.
    """

    user: AbstractBaseUser | AnonymousUser
    session: dict[str, Any] = dataclasses.field(default_factory=dict)
