from __future__ import annotations

import dataclasses
from typing import Any

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser


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


@dataclasses.dataclass
class FakeRequest:
    """
    Minimal mocked request so that import plugins can call ``self.request.user``
    and ``self.request.session`` while running inside a management command.
    """
    user: AbstractBaseUser | AnonymousUser
    session: dict[str, Any] = dataclasses.field(default_factory=dict)
