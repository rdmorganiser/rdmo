from django.utils.functional import cached_property
from django.utils.timezone import now

from rdmo.core.plugins import Plugin
from rdmo.domain.models import Attribute
from rdmo.options.models import Option


class Import(Plugin):
    upload = False
    accept = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = None
        self.now = now()

    @cached_property
    def attributes(self):
        return {attribute.uri: attribute for attribute in Attribute.objects.all()}

    @cached_property
    def options(self):
        return {option.uri: option for option in Option.objects.all()}
