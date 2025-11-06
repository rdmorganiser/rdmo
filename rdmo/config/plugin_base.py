from __future__ import annotations


class PluginBase:

    def __init__(self, key, label, class_name):
        self.key = key
        self.label = label
        self.class_name = class_name
