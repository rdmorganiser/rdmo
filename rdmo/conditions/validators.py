from rdmo.core.validators import UniqueURIValidator


class ConditionUniqueURIValidator(UniqueURIValidator):

    app_label = 'conditions'
    model_name = 'condition'

    def get_uri(self, model, data):
        uri = model.build_uri(data.get('uri_prefix'), data.get('key'))
        return uri
