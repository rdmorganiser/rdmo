from rdmo.core.validators import UniqueURIValidator


class ViewUniqueURIValidator(UniqueURIValidator):

    app_label = 'views'
    model_name = 'view'

    def get_uri(self, model, data):
        uri = model.build_uri(data.get('uri_prefix'), data.get('key'))
        return uri
