from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import gettext_lazy as _

from rdmo.core.utils import join_url
from rdmo.domain.models import Attribute


class Condition(models.Model):

    RELATION_EQUAL = 'eq'
    RELATION_NOT_EQUAL = 'neq'
    RELATION_CONTAINS = 'contains'
    RELATION_GREATER_THAN = 'gt'
    RELATION_GREATER_THAN_EQUAL = 'gte'
    RELATION_LESSER_THAN = 'lt'
    RELATION_LESSER_THAN_EQUAL = 'lte'
    RELATION_EMPTY = 'empty'
    RELATION_NOT_EMPTY = 'notempty'
    RELATION_CHOICES = (
        (RELATION_EQUAL, 'is equal to (==)'),
        (RELATION_NOT_EQUAL, 'is not equal to (!=)'),
        (RELATION_CONTAINS, 'contains'),
        (RELATION_GREATER_THAN, 'is greater than (>)'),
        (RELATION_GREATER_THAN_EQUAL, 'is greater than or equal (>=)'),
        (RELATION_LESSER_THAN, 'is lesser than (<)'),
        (RELATION_LESSER_THAN_EQUAL, 'is lesser than or equal (<=)'),
        (RELATION_EMPTY, 'is empty'),
        (RELATION_NOT_EMPTY, 'is not empty'),
    )

    uri = models.URLField(
        max_length=800, blank=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this condition (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this condition.')
    )
    uri_path = models.SlugField(
        max_length=512, blank=True,
        verbose_name=_('URI Path'),
        help_text=_('The path for the URI of this condition.')
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_('Comment'),
        help_text=_('Additional internal information about this condition.')
    )
    locked = models.BooleanField(
        default=False,
        verbose_name=_('Locked'),
        help_text=_('Designates whether this condition can be changed.')
    )
    editors = models.ManyToManyField(
        Site, related_name='conditions_as_editor', blank=True,
        verbose_name=_('Editors'),
        help_text=_('The sites that can edit this condition (in a multi site setup).')
    )
    source = models.ForeignKey(
        Attribute, blank=True, null=True, on_delete=models.SET_NULL, related_name='conditions',
        db_constraint=False,
        verbose_name=_('Source'),
        help_text=_('The attribute of the value for this condition.')
    )
    relation = models.CharField(
        max_length=8, choices=RELATION_CHOICES,
        verbose_name=_('Relation'),
        help_text=_('The relation this condition is using.')
    )
    target_text = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('Target (Text)'),
        help_text=_('If using a regular value, the text value this condition is checking against '
                    '(for boolean values use 1 and 0).')
    )
    target_option = models.ForeignKey(
        'options.Option', blank=True, null=True, on_delete=models.SET_NULL, related_name='conditions',
        db_constraint=False,
        verbose_name=_('Target (Option)'),
        help_text=_('If using a value pointing to an option, the option this condition is checking against.')
    )

    class Meta:
        ordering = ('uri', )
        verbose_name = _('Condition')
        verbose_name_plural = _('Conditions')

    def __str__(self):
        return self.uri

    def save(self, *args, **kwargs):
        self.uri = self.build_uri(self.uri_prefix, self.uri_path)
        super().save(*args, **kwargs)

    @property
    def source_label(self):
        return self.source.uri

    @property
    def relation_label(self):
        return self.get_relation_display()

    @property
    def target_label(self):
        if self.target_option:
            return self.target_option.label
        else:
            return self.target_text

    @property
    def is_locked(self):
        return self.locked

    def resolve(self, values, set_prefix=None, set_index=None):
        """
        Resolves the condition and returns a detailed result.

        Returns:
            dict: {
                'result': bool,
                'reason': str,
                'trigger_value': Any,
                'trigger_question_url': str
            }
        """
        source_values = self._filter_values(values, set_prefix, set_index)

        if not source_values and set_prefix:
            set_prefix, set_index = self._get_higher_level_prefix(set_prefix)
            return self.resolve(values, set_prefix, set_index)

        resolver_map = {
            self.RELATION_EQUAL: self._resolve_equal,
            self.RELATION_NOT_EQUAL: self._resolve_not_equal,
            self.RELATION_CONTAINS: self._resolve_contains,
            self.RELATION_GREATER_THAN: self._resolve_greater_than,
            self.RELATION_GREATER_THAN_EQUAL: self._resolve_greater_than_equal,
            self.RELATION_LESSER_THAN: self._resolve_lesser_than,
            self.RELATION_LESSER_THAN_EQUAL: self._resolve_lesser_than_equal,
            self.RELATION_EMPTY: self._resolve_empty,
            self.RELATION_NOT_EMPTY: self._resolve_not_empty,
        }

        resolver = resolver_map.get(self.relation)
        if not resolver:
            return {'result': False, 'reason': 'Unknown relation type', 'trigger_value': None,
                    'trigger_question_url': None}

        result = resolver(source_values)

        if result['result']:
            question_url = self._get_question_url(source_values)
            result['trigger_question_url'] = question_url

        return result

    def _get_question_url(self, values):
        """
        Finds the question associated with the resolved value.
        """
        for value in values:
            # Find the first question matching the attribute in the catalog
            question = next(
                (q for q in value.project.catalog.questions if q.attribute == self.source),
                None
            )
            if question:
                return question.get_absolute_url(value)  # Pass the value to `get_absolute_url`
        return None

    def _filter_values(self, values, set_prefix, set_index):
        source_values = filter(lambda value: value.attribute == self.source, values)

        if set_prefix is not None:
            source_values = filter(lambda value: value.set_prefix == set_prefix, source_values)

        if set_index is not None:
            source_values = filter(lambda value: (
                value.set_index == int(set_index) or value.set_collection is False
            ), source_values)

        return list(source_values)

    def _get_higher_level_prefix(self, set_prefix):
        rpartition = set_prefix.rpartition('|')
        return rpartition[0], int(rpartition[2])

    def _resolve_equal(self, values):
        for value in values:
            if self.target_option and value.option == self.target_option:
                return {
                    'result': True,
                    'reason': f"Value matches target option {self.target_option}.",
                    'trigger_value': value.option
                }
            elif not self.target_option and value.text == self.target_text:
                return {
                    'result': True,
                    'reason': f"Value matches target text '{self.target_text}'.",
                    'trigger_value': value.text
                }
        return {'result': False, 'reason': 'No matching value found.', 'trigger_value': None}

    def _resolve_not_equal(self, values):
        for value in values:
            if self.target_option and value.option != self.target_option:
                return {
                    'result': True,
                    'reason': f"Value does not match target option {self.target_option}.",
                    'trigger_value': value.option
                }
            elif not self.target_option and value.text != self.target_text:
                return {
                    'result': True,
                    'reason': f"Value does not match target text '{self.target_text}'.",
                    'trigger_value': value.text
                }
        return {'result': False, 'reason': 'All values match the condition.', 'trigger_value': None}

    def _resolve_contains(self, values):
        for value in values:
            if self.target_text in value.text:
                return {
                    'result': True,
                    'reason': f"Value contains target text '{self.target_text}'.",
                    'trigger_value': value.text
                }
        return {'result': False, 'reason': 'No value contains the target text.', 'trigger_value': None}

    def _resolve_greater_than(self, values):
        for value in values:
            try:
                if float(value.text) > float(self.target_text):
                    return {
                        'result': True,
                        'reason': f"Value {value.text} is greater than target {self.target_text}.",
                        'trigger_value': value.text
                    }
            except ValueError:
                continue
        return {'result': False, 'reason': 'No value is greater than the target.', 'trigger_value': None}

    def _resolve_greater_than_equal(self, values):
        for value in values:
            try:
                if float(value.text) >= float(self.target_text):
                    return {
                        'result': True,
                        'reason': f"Value {value.text} is greater than or equal to target {self.target_text}.",
                        'trigger_value': value.text
                    }
            except ValueError:
                continue
        return {'result': False, 'reason': 'No value is greater than or equal to the target.', 'trigger_value': None}

    def _resolve_lesser_than(self, values):
        for value in values:
            try:
                if float(value.text) < float(self.target_text):
                    return {
                        'result': True,
                        'reason': f"Value {value.text} is less than target {self.target_text}.",
                        'trigger_value': value.text
                    }
            except ValueError:
                continue
        return {'result': False, 'reason': 'No value is less than the target.', 'trigger_value': None}

    def _resolve_lesser_than_equal(self, values):
        for value in values:
            try:
                if float(value.text) <= float(self.target_text):
                    return {
                        'result': True,
                        'reason': f"Value {value.text} is less than or equal to target {self.target_text}.",
                        'trigger_value': value.text
                    }
            except ValueError:
                continue
        return {'result': False, 'reason': 'No value is less than or equal to the target.', 'trigger_value': None}

    def _resolve_empty(self, values):
        for value in values:
            if not value.text and not value.option:
                return {
                    'result': True,
                    'reason': "Value is empty.",
                    'trigger_value': None
                }
        return {'result': False, 'reason': 'All values are non-empty.', 'trigger_value': None}

    def _resolve_not_empty(self, values):
        for value in values:
            if bool(value.text) or bool(value.option):
                return {
                    'result': True,
                    'reason': "Value is not empty.",
                    'trigger_value': value.text or value.option
                }
        return {'result': False, 'reason': 'All values are empty.', 'trigger_value': None}

    @classmethod
    def build_uri(cls, uri_prefix, uri_path):
        if not uri_path:
            raise RuntimeError('uri_path is missing')
        return join_url(uri_prefix or settings.DEFAULT_URI_PREFIX, '/conditions/', uri_path)
