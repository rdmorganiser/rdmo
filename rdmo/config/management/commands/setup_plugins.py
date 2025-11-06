# rdmo/config/management/commands/setup_plugins.py
from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.module_loading import import_string
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from rdmo.config.models import Plugin

# ---------------------------------------------------------------------------#
# Data model (declaration independent from DB rows)
# ---------------------------------------------------------------------------#

@dataclass(frozen=True)
class DeclaredPlugin:
    key: str
    title: str
    python_path: str
    uri_prefix: str | None = None
    uri_path: str | None = None
    plugin_settings: dict[str, Any] | None = None


# ---------------------------------------------------------------------------#
# Legacy settings (deprecated; kept for transition)
# ---------------------------------------------------------------------------#

LEGACY_SETTING_NAMES = (
    "PROJECT_EXPORTS",
    "PROJECT_IMPORTS",
    "PROJECT_SNAPSHOT_EXPORTS",
    "OPTIONSET_PROVIDERS",
    "PROJECT_ISSUE_PROVIDERS",
)

def _iter_legacy_settings() -> list[DeclaredPlugin]:
    """Read 3-tuples (key, label, python-path) from legacy settings."""
    declared: list[DeclaredPlugin] = []

    for setting_name in LEGACY_SETTING_NAMES:
        values = getattr(settings, setting_name, None)
        if not values:
            continue

        for entry in values:
            try:
                key, label, dotted = entry
            except Exception as exc:
                raise CommandError(
                    f"{setting_name} must be a sequence of 3-tuples "
                    f"(key, label, python-path); got {entry!r}"
                ) from exc

            declared.append(
                DeclaredPlugin(
                    key=str(key),
                    title=str(label),
                    python_path=str(dotted),
                    uri_prefix=getattr(settings, "DEFAULT_URI_PREFIX", None),
                    uri_path=f"{setting_name.lower()}/{key}",
                    plugin_settings=_read_per_plugin_settings_from_settings(str(key)),
                )
            )
    return declared


# ---------------------------------------------------------------------------#
# New 2.5 setting: PLUGINS = ['pkg.mod.Class', ...]
# ---------------------------------------------------------------------------#

def _iter_new_setting_plugins() -> list[DeclaredPlugin]:
    """
    Read python paths from settings.PLUGINS and infer key/title.
    Try to import the class to obtain nicer metadata when available.
    """
    paths: list[str] = getattr(settings, "PLUGINS", None) or []
    declared: list[DeclaredPlugin] = []

    for dotted in paths:
        dotted = str(dotted)

        try:
            cls = import_string(dotted)
        except Exception:
            cls = None

        if cls is not None:
            key = getattr(cls, "key", None) or _derive_key_from_class(cls.__name__)
            title = getattr(cls, "label", None) or getattr(cls, "title", None) or cls.__name__
        else:
            class_name = dotted.rsplit(".", 1)[-1]
            key = _derive_key_from_class(class_name)
            title = class_name

        declared.append(
            DeclaredPlugin(
                key=key,
                title=title,
                python_path=dotted,
                uri_prefix=getattr(settings, "DEFAULT_URI_PREFIX", None),
                uri_path=f"plugins/{key}",
                plugin_settings=_read_per_plugin_settings_from_settings(key),
            )
        )

    return declared


def _derive_key_from_class(class_name: str) -> str:
    """
    Turn 'CSVSemicolonExport' -> 'csv_semicolon_export'.
    Stable and readable.
    """
    words = re.findall(r"[A-Z]+(?![a-z])|[A-Z][a-z0-9]*|[a-z0-9]+", class_name)
    snake = "_".join(w.lower() for w in words if w)
    return slugify(snake, allow_unicode=True).replace("-", "_")


# ---------------------------------------------------------------------------#
# XML source (simple and explicit)
# ---------------------------------------------------------------------------#

def _read_xml(path: str) -> list[DeclaredPlugin]:
    """
    Minimal XML format:

    <plugins uri-prefix="https://example.org/rdmo">
      <plugin key="example" title="Example" python-path="pkg.mod.Plugin"
              uri-path="exports/example">
        <settings>{"token": "abc", "sandbox": true}</settings>
      </plugin>
    </plugins>
    """
    root = ET.parse(path).getroot()
    if root.tag != "plugins":
        raise CommandError(f"{path}: root element must be <plugins> (got <{root.tag}>)")
    uri_prefix = root.attrib.get("uri-prefix")

    declared: list[DeclaredPlugin] = []
    for node in root.findall("./plugin"):
        key = _req_attr(node, "key")
        title = _req_attr(node, "title")
        python_path = _req_attr(node, "python-path")
        uri_path = node.attrib.get("uri-path") or f"plugins/{key}"

        # Optional <settings> JSON blob
        settings_node = node.find("./settings")
        plugin_settings: dict[str, Any] = {}
        if settings_node is not None and settings_node.text:
            try:
                plugin_settings = json.loads(settings_node.text)
            except json.JSONDecodeError as exc:
                raise CommandError(f"{path}: <settings> for key={key} is not valid JSON: {exc}") from exc

        declared.append(
            DeclaredPlugin(
                key=key,
                title=title,
                python_path=python_path,
                uri_prefix=uri_prefix or getattr(settings, "DEFAULT_URI_PREFIX", None),
                uri_path=uri_path,
                plugin_settings=plugin_settings,
            )
        )
    return declared


def _req_attr(node: ET.Element, name: str) -> str:
    value = node.attrib.get(name)
    if not value:
        raise CommandError(f"<{node.tag}> is missing required attribute '{name}'")
    return value


# ---------------------------------------------------------------------------#
# Settings resolution (class defaults <- settings <- DB)
# ---------------------------------------------------------------------------#

def _class_defaults(python_path: str) -> dict[str, Any]:
    """
    Optional defaults exposed by the plugin class via DEFAULTS / defaults /
    PLUGIN_DEFAULTS / get_default_settings(). Absent -> {}.

    NB: This intentionally swallows import errors (returns {}), because
    strict validation is handled by the preflight step.
    """
    try:
        cls = import_string(python_path)
    except Exception:
        return {}

    for attr in ("DEFAULTS", "defaults", "PLUGIN_DEFAULTS"):
        value = getattr(cls, attr, None)
        if isinstance(value, dict):
            return value.copy()

    if hasattr(cls, "get_default_settings"):
        try:
            value = cls.get_default_settings()
            if isinstance(value, dict):
                return value.copy()
        except Exception:
            return {}

    return {}


def _read_per_plugin_settings_from_settings(key: str) -> dict[str, Any]:
    """
    Locate per-plugin settings dict in Django settings using robust candidates.
    Candidates (first match wins) include:
      <key>_PROVIDER, <key>_SETTINGS,
      <KEY>_PROVIDER, <KEY>_SETTINGS,
      RDMO_<KEY>_PROVIDER, RDMO_<KEY>_SETTINGS,
      <key.lstrip('rdmo_')>_PROVIDER / _SETTINGS,
      <KEY.lstrip('RDMO_')>_PROVIDER / _SETTINGS
    """
    suffixes = ("_PROVIDER", "_SETTINGS")
    keys = (key, key.upper(), key.lstrip("rdmo_"), key.lstrip("RDMO_"))

    candidates: list[str] = []
    for base in keys:
        if not base:
            continue
        for suffix in suffixes:
            candidates.append(f"{base}{suffix}")
            candidates.append(f"RDMO_{str(base).upper()}{suffix}")

    for name in candidates:
        if hasattr(settings, name):
            val = getattr(settings, name)
            if isinstance(val, dict):
                return val.copy()

    return {}


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """
    Recursively merge dictionaries. Values in `override` replace those in `base`.
    Lists are replaced wholesale (predictable, avoids accidental concatenation).
    """
    out: dict[str, Any] = {}
    for k in base.keys() | override.keys():
        bv = base.get(k)
        ov = override.get(k)
        if isinstance(bv, dict) and isinstance(ov, dict):
            out[k] = _deep_merge(bv, ov)
        elif k in override:
            out[k] = ov
        else:
            out[k] = bv
    return out


def _resolved_settings(declared: DeclaredPlugin, existing_db: dict[str, Any] | None) -> dict[str, Any]:
    """
    Merge chain:
        class defaults  <-  settings.py/env  <-  DB JSON
    DB wins last.
    """
    class_def = _class_defaults(declared.python_path)
    from_settings = declared.plugin_settings or {}
    from_db = existing_db or {}
    return _deep_merge(_deep_merge(class_def, from_settings), from_db)


# ---------------------------------------------------------------------------#
# Validation, clearing & persistence
# ---------------------------------------------------------------------------#

def _validate_import(python_path: str) -> None:
    """Strict import check used during preflight. Raises CommandError on failure."""
    try:
        import_string(python_path)
    except Exception as exc:
        raise CommandError(f'Could not import class: {python_path} ({exc})') from exc


def _clear_plugins(*, dry_run: bool, stdout, style, force: bool) -> None:
    """
    Clear all Plugin rows. In dry-run, print what would be deleted.
    Without --force (and not dry-run), prompt for confirmation.
    """
    qs = Plugin.objects.all().order_by("uri_prefix", "uri_path")
    count = qs.count()

    if count == 0:
        stdout.write(style.WARNING("⚠ no Plugin objects found; nothing to clear."))
        return

    stdout.write(style.WARNING(f"⚠ about to clear {count} Plugin object(s):"))
    for p in qs:
        if dry_run:
            stdout.write(style.WARNING(f"• {p.python_path} at {p.uri} will be deleted"))
        else:
            stdout.write(style.WARNING(f"• {p.python_path} at {p.uri} marked for deletion"))

    if dry_run:
        return

    if not force:
        stdout.write("")
        stdout.write(style.WARNING("Type 'yes' to confirm deletion of ALL Plugin objects: "), ending="")
        try:
            confirm = input().strip().lower()
        except EOFError:
            confirm = ""
        if confirm != "yes":
            raise CommandError("Clear aborted by user.")

    deleted, _ = qs.delete()
    stdout.write(style.SUCCESS(f"✔ deleted {deleted} object(s)."))


def _upsert_plugin(declared: DeclaredPlugin, *, replace: bool, dry_run: bool) -> tuple[Plugin | None, str]:
    uri_prefix = declared.uri_prefix or getattr(settings, "DEFAULT_URI_PREFIX", None)
    if not uri_prefix:
        raise CommandError("No uri_prefix available (neither in XML nor DEFAULT_URI_PREFIX).")

    uri_path = declared.uri_path or f"plugins/{declared.key}"

    try:
        plugin = Plugin.objects.get(uri_prefix=uri_prefix, uri_path=uri_path)
        exists = True
    except Plugin.DoesNotExist:
        plugin = Plugin(uri_prefix=uri_prefix, uri_path=uri_path)
        exists = False

    # Merge settings (DB wins last)
    plugin_settings = _resolved_settings(declared, plugin.plugin_settings if exists else None)

    # Update fields
    plugin.title_lang1 = declared.title
    plugin.python_path = declared.python_path
    plugin.plugin_settings = plugin_settings
    plugin.available = True

    action = "replaced" if (exists and replace) else ("updated" if exists else "created")
    if dry_run:
        return None, f"{action} (dry-run): {declared.python_path} -> {uri_path}"

    if exists and replace:
        # reset a few mutable fields (keeps M2M untouched)
        plugin.comment = ""
        plugin.locked = False
        plugin.order = 0

    plugin.full_clean()
    plugin.save()  # model computes canonical .uri via build_uri()
    return plugin, f"{action}: {plugin.python_path} -> {plugin.uri}"


# ---------------------------------------------------------------------------#
# Command
# ---------------------------------------------------------------------------#

class Command(BaseCommand):
    help = _("Create or update Plugin objects from PLUGINS, legacy settings, or XML. Can also clear all plugins.")

    def add_arguments(self, parser):
        parser.add_argument(
            "--from-settings",
            action="store_true",
            help=_("Load plugin declarations from deprecated Django settings."),
        )
        parser.add_argument(
            "--from-xml",
            metavar="PATH",
            action="append",
            help=_("Load plugin declarations from XML file(s). May be given multiple times."),
        )
        parser.add_argument(
            "--replace",
            action="store_true",
            help=_("Replace existing rows instead of updating fields incrementally."),
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help=_("Do not write to the database, only print intended actions."),
        )
        parser.add_argument(
            "--no-validate",
            action="store_true",
            help=_("Skip strict preflight import checks (not recommended)."),
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help=_("Delete ALL existing Plugin objects before importing."),
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help=_("Do not prompt for confirmation when using --clear."),
        )

    @transaction.atomic
    def handle(self, *args, **options):
        from_settings_flag: bool = options["from_settings"]
        xml_paths: list[str] | None = options["from_xml"]
        replace: bool = options["replace"]
        dry_run: bool = options["dry_run"]
        no_validate: bool = options["no_validate"]
        do_clear: bool = options["clear"]
        force: bool = options["force"]

        declared: list[DeclaredPlugin] = []

        # Optional destructive phase first
        if do_clear:
            self.stdout.write(self.style.WARNING("⚠ --clear requested: ALL Plugin objects will be removed."))
            _clear_plugins(dry_run=dry_run, stdout=self.stdout, style=self.style, force=force)

        # Collect declarations
        if from_settings_flag:
            declared.extend(_iter_legacy_settings())
            declared.extend(_iter_new_setting_plugins())
        if xml_paths:
            for path in xml_paths:
                declared.extend(_read_xml(path))

        # If no import source and only --clear, we are done.
        if not declared:
            if do_clear:
                if dry_run:
                    # Make it explicit that nothing changed.
                    raise CommandError("Dry-run complete; no changes committed.")
                self.stdout.write(self.style.SUCCESS("✔ clear completed."))
                return
            raise CommandError(
                "Nothing to do. Use --clear and/or one of --from-plugins/--from-settings/--from-xml PATH."
            )

        if from_settings_flag:
            self.stdout.write(self.style.WARNING(
                "Reading legacy plugin settings. These are deprecated and will be removed in a future release."
            ))

        # Deterministic order for output
        declared.sort(key=lambda d: (d.uri_path or "", d.python_path))

        # -------------------- Preflight validation --------------------------
        if not no_validate:
            errors: list[tuple[DeclaredPlugin, Exception]] = []
            for d in declared:
                try:
                    _validate_import(d.python_path)
                    self.stdout.write(self.style.SUCCESS(f"✔ import OK: {d.python_path}"))
                except Exception as exc:
                    errors.append((d, exc))
                    self.stdout.write(self.style.ERROR(f"✖ import FAILED: {d.python_path} ({exc})"))

            if errors:
                raise CommandError(
                    f"{len(errors)} plugin(s) failed preflight import; aborting before database changes."
                )

        # -------------------- Upsert phase ---------------------------------
        results: list[str] = []
        for d in declared:
            try:
                _, msg = _upsert_plugin(d, replace=replace, dry_run=dry_run)
                results.append(self.style.SUCCESS(f"✔ {msg}"))
            except Exception as exc:
                results.append(self.style.ERROR(f"✖ {d.python_path} failed: {exc}"))

        for line in results:
            self.stdout.write(line)

        if dry_run:
            # Roll back on purpose in dry-run mode
            raise CommandError("Dry-run complete; no changes committed.")
