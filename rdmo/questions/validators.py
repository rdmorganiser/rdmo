from rdmo.core.validators import UniqueKeyValidator, UniquePathValidator


class CatalogUniqueKeyValidator(UniqueKeyValidator):

    app_label = 'questions'
    model_name = 'catalog'


class SectionUniquePathValidator(UniquePathValidator):

    app_label = 'questions'
    model_name = 'section'

    def get_path(self, model, data):
        return model.build_path(data['key'], data['catalog'])


class SubsectionUniquePathValidator(UniquePathValidator):

    app_label = 'questions'
    model_name = 'subsection'

    def get_path(self, model, data):
        return model.build_path(data['key'], data['section'])


class QuestionEntityUniquePathValidator(UniquePathValidator):

    app_label = 'questions'
    model_name = 'questionentity'

    def get_path(self, model, data):
        return model.build_path(data['key'], data['subsection'])


class QuestionUniquePathValidator(UniquePathValidator):

    app_label = 'questions'
    model_name = 'questionentity'

    def get_path(self, model, data):
        try:
            return model.build_path(data['key'], data['subsection'], data['parent'])
        except KeyError:
            return model.build_path(data['key'], data['subsection'])
