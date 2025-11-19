from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from django.utils.module_loading import import_string


@dataclass(frozen=True)
class DeclaredPlugin:
    uri_prefix: str
    uri_path: str  # is the key for legacy settings
    python_path: str
    title: str = field(repr=False)
    plugin_type: str
    plugin_settings: dict[str, Any] | None = field(default_factory=dict, repr=False)
    url_name: str | None = ""  # also the key for legacy settings
    source: str | None = None  # from legacy setting or db

    def get_plugin_instance(self):
        try:
            return import_string(self.python_path)(self.uri_path, self.title, self.python_path)
        except Exception:
            return None
