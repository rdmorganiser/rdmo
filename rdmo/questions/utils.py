from rdmo.core.plugins import get_plugin, get_plugins


def get_widgets():
    widgets = get_plugins('QUESTIONS_WIDGETS')
    return widgets.values()


def get_widget_types():
    widgets = get_plugins('QUESTIONS_WIDGETS')
    return [widget.key for widget in widgets.values()]


def get_widget_type_choices():
    widgets = get_plugins('QUESTIONS_WIDGETS')
    return [(widget.key, widget.label) for widget in widgets.values()]


def get_widget_class(key):
    widget = get_plugin('QUESTIONS_WIDGETS', key)
    return widget.widget_class
