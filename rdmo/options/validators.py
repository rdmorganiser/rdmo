from rdmo.core.validators import UniqueKeyValidator, UniquePathValidator


class OptionSetUniqueKeyValidator(UniqueKeyValidator):

    app_label = 'options'
    model_name = 'optionset'


class OptionUniquePathValidator(UniquePathValidator):

    app_label = 'options'
    model_name = 'option'

    def get_path(self, model, data):
        return model.build_path(data['key'], data['optionset'])
