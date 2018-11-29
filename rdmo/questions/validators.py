from rdmo.core.validators import UniqueKeyValidator, UniquePathValidator


class CatalogUniqueKeyValidator(UniqueKeyValidator):

    app_label = 'questions'
    model_name = 'catalog'


class SectionUniquePathValidator(UniquePathValidator):

    app_label = 'questions'
    model_name = 'section'

    def get_path(self, model, data):
        return model.build_path(data['key'], data['catalog'])


class QuestionSetUniquePathValidator(UniquePathValidator):

    app_label = 'questions'
    model_name = 'questionset'

    def get_path(self, model, data):
        return model.build_path(data['key'], data['section'])


class QuestionUniquePathValidator(UniquePathValidator):

    app_label = 'questions'
    model_name = 'question'

    def get_path(self, model, data):
        return model.build_path(data['key'], data['questionset'])
