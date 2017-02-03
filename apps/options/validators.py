from apps.core.validators import UniquePathValidator


class OptionUniquePathValidator(UniquePathValidator):

    app_label = 'options'
    model_name = 'option'

    def get_path(self, model, data):
        return model.build_path(data['key'], data['optionset'])
