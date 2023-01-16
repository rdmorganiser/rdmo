from django.utils.translation import gettext_lazy as _

from rdmo.core.validators import (InstanceValidator, LockedValidator,
                                  UniqueURIValidator)

from .models import Catalog, Page, Question, QuestionSet, Section


class CatalogUniqueURIValidator(UniqueURIValidator):

    model = Catalog
    models = (Catalog, Section, Page, QuestionSet, Question)


class SectionUniqueURIValidator(UniqueURIValidator):

    model = Section
    models = (Catalog, Section, Page, QuestionSet, Question)


class PageUniqueURIValidator(UniqueURIValidator):

    model = Page
    models = (Catalog, Section, Page, QuestionSet, Question)


class QuestionSetUniqueURIValidator(UniqueURIValidator):

    model = QuestionSet
    models = (Catalog, Section, Page, QuestionSet, Question)


class QuestionUniqueURIValidator(UniqueURIValidator):

    model = Question
    models = (Catalog, Section, Page, QuestionSet, Question)


class QuestionSetQuestionSetValidator(InstanceValidator):

    def __call__(self, data):
        questionset = data.get('questionset')
        if questionset:
            if self.serializer:
                # check copied attributes
                view = self.serializer.context.get('view')
                if view and view.action == 'copy':
                    # get the original from the view when cloning an attribute
                    if questionset in view.get_object().get_descendants(include_self=True):
                        self.raise_validation_error({
                            'questionset': [_('A question set may not be cloned to be a child of itself or one of its descendants.')]
                        })

            # only check updated attributes
            if self.instance:
                if questionset in self.instance.get_descendants(include_self=True):
                    self.raise_validation_error({
                        'questionset': [_('A question set may not be moved to be a child of itself or one of its descendants.')]
                    })


class CatalogLockedValidator(LockedValidator):

    pass


class SectionLockedValidator(LockedValidator):

    parent_field = 'catalog'


class PageLockedValidator(LockedValidator):

    parent_field = 'section'


class QuestionSetLockedValidator(LockedValidator):

    parent_field = 'page'


class QuestionLockedValidator(LockedValidator):

    parent_field = 'page'
