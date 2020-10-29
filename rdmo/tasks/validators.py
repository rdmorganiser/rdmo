from rdmo.core.validators import UniqueURIValidator


class TaskUniqueURIValidator(UniqueURIValidator):

    app_label = 'tasks'
    model_name = 'task'

    def get_uri(self, model, data):
        uri = model.build_uri(data.get('uri_prefix'), data.get('key'))
        return uri
