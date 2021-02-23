from django.utils.translation import ugettext_lazy as _

from rdmo.core.validators import LockedValidator, UniqueURIValidator

from .models import Catalog, Question, QuestionSet, Section


class CatalogUniqueURIValidator(UniqueURIValidator):

    model = Catalog

    def get_uri(self, data):
        if data.get('key') is None:
            self.raise_validation_error({'key': _('This field is required.')})
        else:
            uri = self.model.build_uri(data.get('uri_prefix'), data.get('key'))
            return uri


class SectionUniqueURIValidator(UniqueURIValidator):

    model = Section

    def get_uri(self, data):
        if data.get('key') is None:
            self.raise_validation_error({'key': _('This field is required.')})
        elif data.get('catalog') is None:
            self.raise_validation_error({'catalog': _('This field may not be null.')})
        else:
            path = self.model.build_path(data.get('key'), data.get('catalog'))
            uri = self.model.build_uri(data.get('uri_prefix'), path)
            return uri


class QuestionSetUniqueURIValidator(UniqueURIValidator):

    model = QuestionSet

    def get_uri(self, data):
        if data.get('key') is None:
            self.raise_validation_error({'key': _('This field is required.')})
        elif data.get('section') is None:
            self.raise_validation_error({'section': _('This field may not be null.')})
        else:
            path = self.model.build_path(data.get('key'), data.get('section'))
            uri = self.model.build_uri(data.get('uri_prefix'), path)
            return uri


class QuestionUniqueURIValidator(UniqueURIValidator):

    model = Question

    def get_uri(self, data):
        if data.get('key') is None:
            self.raise_validation_error({'key': _('This field is required.')})
        elif data.get('questionset') is None:
            self.raise_validation_error({'questionset': _('This field may not be null.')})
        else:
            path = self.model.build_path(data.get('key'), data.get('questionset'))
            uri = self.model.build_uri(data.get('uri_prefix'), path)
            return uri


class CatalogLockedValidator(LockedValidator):

    pass


class SectionLockedValidator(LockedValidator):

    parent_field = 'catalog'


class QuestionSetLockedValidator(LockedValidator):

    parent_field = 'section'


class QuestionLockedValidator(LockedValidator):

    parent_field = 'questionset'
