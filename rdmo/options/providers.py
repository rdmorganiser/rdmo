from rdmo.config.plugins import BasePlugin


class Provider(BasePlugin):

    plugin_type = 'optionset_provider'

    # determines if the provider supports "live searching" via autocomplete
    search = False

    # determines if the page needs to be refreshed after a value is stored
    refresh = False

    def get_options(self, project, search=None, user=None, site=None):
        raise NotImplementedError
