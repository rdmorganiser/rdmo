class BaseProvider():

    def __init__(self, key, label, class_name):
        self.key = key
        self.label = label
        self.class_name = class_name

    def get_options(self, project):
        raise NotImplementedError


class SimpleProvider(BaseProvider):

    def get_options(self, project):
        return [
            {
                'external_id': 'simple_1',
                'text': 'Simple answer 1'
            },
            {
                'external_id': 'simple_2',
                'text': 'Simple answer 2'
            },
            {
                'external_id': 'simple_3',
                'text': 'Simple answer 3'
            }
        ]
