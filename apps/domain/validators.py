from apps.core.validators import UniquePathValidator


class AttributeEntityUniquePathValidator(UniquePathValidator):

    app_label = 'domain'
    model_name = 'attributeentity'

    def get_path(self, model, data):
        return model.build_path(data['key'], data['parent'])
