from rdmo.core.validators import UniqueKeyValidator


class ConditionUniqueKeyValidator(UniqueKeyValidator):

    app_label = 'conditions'
    model_name = 'condition'
