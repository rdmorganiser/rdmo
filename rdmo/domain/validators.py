from rdmo.core.validators import UniquePathValidator


class AttributeUniquePathValidator(UniquePathValidator):

    app_label = 'domain'
    model_name = 'attribute'

    def get_path(self, model, data):
        return model.build_path(data['key'], data['parent'])
