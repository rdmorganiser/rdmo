from rdmo.core.plugins import Plugin


class Provider(Plugin):

    def get_options(self, project):
        raise NotImplementedError


class SimpleProvider(Provider):

    def get_options(self, project):
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
