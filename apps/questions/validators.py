from apps.core.validators import UniqueLabelSerializerValidator

from .models import Section, Subsection, QuestionEntity, Question


class SectionUniqueLabelSerializerValidator(UniqueLabelSerializerValidator):

    def get_model(self):
        return Section

    def get_label(self, data):
        return Section.build_label(data['key'], data['catalog'])


class SubsectionUniqueLabelSerializerValidator(UniqueLabelSerializerValidator):

    def get_model(self):
        return Subsection

    def get_label(self, data):
        return Subsection.build_label(data['key'], data['section'])


class QuestionEntityUniqueLabelSerializerValidator(UniqueLabelSerializerValidator):

    def get_model(self):
        return QuestionEntity

    def get_label(self, data):
        return QuestionEntity.build_label(data['key'], data['subsection'])


class QuestionUniqueLabelSerializerValidator(UniqueLabelSerializerValidator):

    def get_model(self):
        return QuestionEntity

    def get_label(self, data):
        return Question.build_label(data['key'], data['subsection'], data['parent'])
