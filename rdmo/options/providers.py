from rdmo.core.plugins import Plugin


class Provider(Plugin):

    # determines if the provider supports "live searching" via autocomplete
    search = False

    # determines if the page needs to be refreshed after a value is stored
    refresh = False

    def get_options(self, project, search=None, user=None, site=None):
        raise NotImplementedError
