from rdmo.options.providers import Provider


class SimpleProvider(Provider):
    default_uri_prefix = "https://rdmorganiser.github.io/terms"
    refresh = True

    def get_options(self, project, search=None, user=None, site=None):
        return [
            {
                'id': 'simple_1',
                'text': 'Simple answer 1',
                'help': 'One'
            },
            {
                'id': 'simple_2',
                'text': 'Simple answer 2',
                'help': 'Two'
            },
            {
                'id': 'simple_3',
                'text': 'Simple answer 3',
                'help': 'Three'
            }
        ]
