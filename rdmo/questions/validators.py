from django.utils.translation import gettext_lazy as _

from rdmo.core.validators import InstanceValidator, LockedValidator, UniqueURIValidator

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

    def __call__(self, data, serializer=None):
        super().__call__(data, serializer)

        questionsets = data.get('questionsets')
        if not questionsets:
            return

        if not self.serializer and not self.instance:
            return

        if self.serializer:
            # check copied attributes
            view = self.serializer.context.get('view')
            if view and view.action == 'copy':
                # get the original from the view when cloning an attribute
                obj = view.get_object()
                for questionset in questionsets:
                    if obj in [questionset, *questionset.descendants]:
                        self.raise_validation_error({
                            'questionset': [_('A question set may not be cloned to be a child of itself or one of '
                                              'its descendants.')]
                        })
            if not self.instance:
                return

        # only check updated attributes
        if not self.instance:
            return

        for questionset in questionsets:
            if self.instance in [questionset, *questionset.descendants]:
                self.raise_validation_error({
                    'questionsets': [_('A question set may not be a child of itself or one of its descendants.')]
                })


class CatalogLockedValidator(LockedValidator):

    pass


class SectionLockedValidator(LockedValidator):

    parent_fields = ('catalogs', )


class PageLockedValidator(LockedValidator):

    parent_fields = ('sections', )


class QuestionSetLockedValidator(LockedValidator):

    parent_fields = ('pages', 'parents')


class QuestionLockedValidator(LockedValidator):

    parent_fields = ('pages', 'questionsets')
