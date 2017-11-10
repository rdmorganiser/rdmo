from rdmo.core.validators import UniquePathValidator


class AttributeEntityUniquePathValidator(UniquePathValidator):

    app_label = 'domain'
    model_name = 'attributeentity'

    def get_path(self, model, data):
        try:
            return model.build_path(data['key'], data['parent'])
        except KeyError:
            return model.build_path(data['key'], None)
