from rdmo.core.validators import UniqueKeyValidator


class ViewUniqueKeyValidator(UniqueKeyValidator):

    app_label = 'views'
    model_name = 'view'
