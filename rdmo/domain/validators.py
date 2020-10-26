from rdmo.core.validators import UniqueURIValidator


class AttributeUniqueURIValidator(UniqueURIValidator):

    app_label = 'domain'
    model_name = 'attribute'

    def get_uri(self, model, data):
        path = model.build_path(data.get('key'), data.get('parent'))
        uri = model.build_uri(data.get('uri_prefix'), path)
        return uri
