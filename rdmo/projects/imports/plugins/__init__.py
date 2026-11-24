from django.utils.timezone import now

from rdmo.core.plugins import Plugin
from rdmo.domain.models import Attribute
from rdmo.options.models import Option


class Import(Plugin):

    accept = None
    upload = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = None
        self.now = now()
        self.attributes = {attribute.uri: attribute for attribute in Attribute.objects.all()}
        self.options = {option.uri: option for option in Option.objects.all()}
