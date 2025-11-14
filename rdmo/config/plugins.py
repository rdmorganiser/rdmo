from __future__ import annotations

from django.conf import settings

from rdmo.config.helpers import DeclaredPlugin
from rdmo.config.models import Plugin


def get_plugins_from_db(project=None, plugin_type: str | None=None, user=None) -> list[DeclaredPlugin]:
    """
    Pull available plugins for the given project, then keep only rows whose class
    inherits the correct base (e.g. Import/Export/Provider).
    """
    if not settings.PLUGINS:
        return []

    qs = Plugin.objects.for_context(
        project=project,
        plugin_type=plugin_type,
        user=user,
    ).order_by("order", "uri")

    results: list[DeclaredPlugin] = []
    for instance in qs:

        try:
            _ = instance.clean()  # raises if import_string fails;
        except Exception:
            continue

        if instance.python_path not in settings.PLUGINS:
            continue

        if instance.plugin_type != plugin_type:
            continue

        results.append(DeclaredPlugin(
            uri_prefix=instance.uri_prefix,
            uri_path=instance.uri_path,
            python_path=instance.python_path,
            title=instance.title or instance.uri_path,
            plugin_type=instance.plugin_type,
            url_name=instance.url_name,
            source=f"Plugin(id={instance.id})",
        ))
    return results
