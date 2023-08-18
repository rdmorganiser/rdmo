from rdmo.core.plugins import Plugin


class Provider(Plugin):

    # determines if the provider supports "live searching" via autocomplete
    search = False

    # determines if the page needs to be refreshed after a value is stored
    refresh = False

    def get_options(self, project, search=None):
        raise NotImplementedError


class SimpleProvider(Provider):

    def get_options(self, project, search=None):
        return [
            {
                'id': 'simple_1',
                'text': 'Simple answer 1'
            },
            {
                'id': 'simple_2',
                'text': 'Simple answer 2'
            },
            {
                'id': 'simple_3',
                'text': 'Simple answer 3'
            }
        ]
