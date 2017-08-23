from rdmo.core.validators import UniqueKeyValidator


class TaskUniqueKeyValidator(UniqueKeyValidator):

    app_label = 'tasks'
    model_name = 'task'
