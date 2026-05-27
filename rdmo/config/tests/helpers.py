import sys
import types


def _install_dummy_plugin(monkeypatch, dotted: str = "dummy_mod.DummyPlugin", **attrs) -> str:
    """
    Create a dummy importable plugin class at the dotted path.
    Returns the dotted path string for convenience.
    """
    module_name, class_name = dotted.rsplit(".", 1)
    mod = types.ModuleType(module_name)
    cls = type(class_name, (), {"__module__": module_name})
    # sensible defaults that the command can read if it imports the class
    cls.key = attrs.get("key", "dummy_key")
    cls.label = attrs.get("label", "Dummy Label")
    cls.plugin_type = attrs.get("plugin_type", "dummy_type")
    mod.__dict__[class_name] = cls
    monkeypatch.setitem(sys.modules, module_name, mod)
    return dotted
