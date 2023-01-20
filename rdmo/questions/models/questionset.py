from django.conf import settings
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from rdmo.conditions.models import Condition
from rdmo.core.models import Model, TranslationMixin
from rdmo.core.utils import copy_model, join_url
from rdmo.domain.models import Attribute


class QuestionSet(Model, TranslationMixin):

    uri = models.URLField(
        max_length=800, blank=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this question set (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this question set.')
    )
    uri_path = models.CharField(
        max_length=512, blank=True,
        verbose_name=_('URI Path'),
        help_text=_('The path for the URI of this question set.')
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_('Comment'),
        help_text=_('Additional internal information about this question set.')
    )
    locked = models.BooleanField(
        default=False,
        verbose_name=_('Locked'),
        help_text=_('Designates whether this question set (and its questions) can be changed.')
    )
    attribute = models.ForeignKey(
        Attribute, blank=True, null=True, related_name='questionsets',
        on_delete=models.SET_NULL,
        verbose_name=_('Attribute'),
        help_text=_('The attribute this question set belongs to.')
    )
    questionsets = models.ManyToManyField(
        'QuestionSet', blank=True, related_name='parents',
        verbose_name=_('Question sets'),
        help_text=_('The question sets of this question set.')
    )
    questions = models.ManyToManyField(
        'Question', blank=True, related_name='questionsets',
        verbose_name=_('Questions'),
        help_text=_('The questions of this question set.')
    )
    is_collection = models.BooleanField(
        default=False,
        verbose_name=_('is collection'),
        help_text=_('Designates whether this question set is a collection.')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('The position of this question set in lists.')
    )
    title_lang1 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (primary)'),
        help_text=_('The title for this question set in the primary language.')
    )
    title_lang2 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (secondary)'),
        help_text=_('The title for this question set in the secondary language.')
    )
    title_lang3 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (tertiary)'),
        help_text=_('The title for this question set in the tertiary language.')
    )
    title_lang4 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (quaternary)'),
        help_text=_('The title for this question set in the quaternary language.')
    )
    title_lang5 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Title (quinary)'),
        help_text=_('The title for this question set in the quinary language.')
    )
    help_lang1 = models.TextField(
        blank=True,
        verbose_name=_('Help (primary)'),
        help_text=_('The help text for this question set in the primary language.')
    )
    help_lang2 = models.TextField(
        blank=True,
        verbose_name=_('Help (secondary)'),
        help_text=_('The help text for this question set in the secondary language.')
    )
    help_lang3 = models.TextField(
        blank=True,
        verbose_name=_('Help (tertiary)'),
        help_text=_('The help text for this question set in the tertiary language.')
    )
    help_lang4 = models.TextField(
        blank=True,
        verbose_name=_('Help (quaternary)'),
        help_text=_('The help text for this question set in the quaternary language.')
    )
    help_lang5 = models.TextField(
        blank=True,
        verbose_name=_('Help (quinary)'),
        help_text=_('The help text for this question set in the quinary language.')
    )
    verbose_name_lang1 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Name (primary)'),
        help_text=_('The name displayed for this question set in the primary language.')
    )
    verbose_name_lang2 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Name (secondary)'),
        help_text=_('The name displayed for this question set in the secondary language.')
    )
    verbose_name_lang3 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Name (tertiary)'),
        help_text=_('The name displayed for this question set in the tertiary language.')
    )
    verbose_name_lang4 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Name (quaternary)'),
        help_text=_('The name displayed for this question set in the quaternary language.')
    )
    verbose_name_lang5 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Name (quinary)'),
        help_text=_('The name displayed for this question set in the quinary language.')
    )
    verbose_name_plural_lang1 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Plural name (primary)'),
        help_text=_('The plural name displayed for this question set in the primary language.')
    )
    verbose_name_plural_lang2 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Plural name (secondary)'),
        help_text=_('The plural name displayed for this question set in the secondary language.')
    )
    verbose_name_plural_lang3 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Plural name (tertiary)'),
        help_text=_('The plural name displayed for this question set in the tertiary language.')
    )
    verbose_name_plural_lang4 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Plural name (quaternary)'),
        help_text=_('The plural name displayed for this question set in the quaternary language.')
    )
    verbose_name_plural_lang5 = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Plural name (quinary)'),
        help_text=_('The plural name displayed for this question set in the quinary language.')
    )
    conditions = models.ManyToManyField(
        Condition, blank=True, related_name='questionsets',
        verbose_name=_('Conditions'),
        help_text=_('List of conditions evaluated for this question set.')
    )

    class Meta:
        ordering = ('uri', )
        verbose_name = _('Question set')
        verbose_name_plural = _('Question set')

    def __str__(self):
        return self.uri

    def save(self, *args, **kwargs):
        self.uri = self.build_uri(self.uri_prefix, self.uri_path)

        super().save(*args, **kwargs)

        for questionset in self.questionsets.all():
            questionset.save()
        for question in self.questions.all():
            question.save()

    def copy(self, uri_prefix, uri_path):
        questionset = copy_model(self, uri_prefix=uri_prefix, uri_path=uri_path, attribute=self.attribute)

        # copy m2m fields
        questionset.questionsets.set(self.questionsets.all())
        questionset.questions.set(self.questions.all())
        questionset.conditions.set(self.conditions.all())

        return questionset

    @property
    def parent_fields(self):
        return ('page', 'questionset')

    @property
    def title(self):
        return self.trans('title')

    @property
    def help(self):
        return self.trans('help')

    @property
    def verbose_name(self):
        return self.trans('verbose_name')

    @property
    def verbose_name_plural(self):
        return self.trans('verbose_name_plural')

    @property
    def is_locked(self):
        return self.locked or \
            any([page.is_locked for page in self.pages.all()]) or \
            any([questionset.is_locked for questionset in self.questionsets.all()])

    @property
    def is_question(self):
        return False

    @property
    def has_conditions(self):
        return self.conditions.exists()

    @cached_property
    def elements(self):
        elements = list(self.questionsets.all()) + list(self.questions.all())
        return sorted(elements, key=lambda e: e.order)

    def get_descendants(self, include_self=False):
        # this function tries to mimic the same function from mptt
        descendants = [self] if include_self else []
        for element in self.elements:
            if element.is_question:
                descendants.append(element)
            else:
                descendants += element.get_descendants(include_self=True)
        return descendants

    def get_ancestors(self, ascending=False, include_self=False):
        # this function tries to mimic the same function from mptt
        ancestors = []

        if include_self:
            ancestors.append(self)

        if self.questionset:
            ancestors += self.questionset.get_ancestors(ascending=True, include_self=True)

        if not ascending:
            ancestors.reverse()

        return ancestors

    @classmethod
    def build_uri(cls, uri_prefix, uri_path):
        if not uri_path:
            raise RuntimeError('uri_path is missing')
        return join_url(uri_prefix or settings.DEFAULT_URI_PREFIX, '/questions/', uri_path)
