from rdmo.core.validators import UniqueURIValidator


class CatalogUniqueURIValidator(UniqueURIValidator):

    app_label = 'questions'
    model_name = 'catalog'

    def get_uri(self, model, data):
        uri = model.build_uri(data.get('uri_prefix'), data.get('key'))
        return uri


class SectionUniqueURIValidator(UniqueURIValidator):

    app_label = 'questions'
    model_name = 'section'

    def get_uri(self, model, data):
        path = model.build_path(data.get('key'), data.get('catalog'))
        uri = model.build_uri(data.get('uri_prefix'), path)
        return uri


class QuestionSetUniqueURIValidator(UniqueURIValidator):

    app_label = 'questions'
    model_name = 'questionset'

    def get_uri(self, model, data):
        path = model.build_path(data.get('key'), data.get('section'))
        uri = model.build_uri(data.get('uri_prefix'), path)
        return uri


class QuestionUniqueURIValidator(UniqueURIValidator):

    app_label = 'questions'
    model_name = 'question'

    def get_uri(self, model, data):
        path = model.build_path(data.get('key'), data.get('questionset'))
        uri = model.build_uri(data.get('uri_prefix'), path)
        return uri
