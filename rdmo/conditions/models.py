from django.db import models
from django.utils.translation import ugettext_lazy as _

from rdmo.core.utils import get_uri_prefix
from rdmo.domain.models import Attribute

from .validators import ConditionUniqueKeyValidator


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
        max_length=640, blank=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this condition (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this condition.')
    )
    key = models.SlugField(
        max_length=128, blank=True,
        verbose_name=_('Key'),
        help_text=_('The internal identifier of this condition.')
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_('Comment'),
        help_text=_('Additional internal information about this condition.')
    )
    source = models.ForeignKey(
        Attribute, db_constraint=False, blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
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
        help_text=_('If using a regular value, the text value this condition is checking against (for boolean values use 1 and 0).')
    )
    target_option = models.ForeignKey(
        'options.Option', db_constraint=False, blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
        verbose_name=_('Target (Option)'),
        help_text=_('If using a value pointing to an option, the option this condition is checking against.')
    )

    class Meta:
        ordering = ('uri', )
        verbose_name = _('Condition')
        verbose_name_plural = _('Conditions')

    def __str__(self):
        return self.key

    def clean(self):
        ConditionUniqueKeyValidator(self).validate()

    @property
    def source_path(self):
        return self.source.path

    @property
    def relation_label(self):
        return dict(self.RELATION_CHOICES)[self.relation]

    @property
    def target_label(self):
        if self.target_option:
            return self.target_option.text
        else:
            return self.target_text

    def save(self, *args, **kwargs):
        self.uri = self.build_uri()
        super(Condition, self).save(*args, **kwargs)

    def build_uri(self):
        return get_uri_prefix(self) + '/conditions/' + self.key

    def resolve(self, project, snapshot=None):
        # get the values for the given project, the given snapshot and the condition's attribute
        values = project.values.filter(snapshot=snapshot).filter(attribute=self.source)

        if self.relation == self.RELATION_EQUAL:
            return self._resolve_equal(values)

        elif self.relation == self.RELATION_NOT_EQUAL:
            return not self._resolve_equal(values)

        elif self.relation == self.RELATION_CONTAINS:
            return self._resolve_contains(values)

        elif self.relation == self.RELATION_GREATER_THAN:
            return self._resolve_greater_than(values)

        elif self.relation == self.RELATION_GREATER_THAN_EQUAL:
            return self._resolve_greater_than_equal(values)

        elif self.relation == self.RELATION_LESSER_THAN:
            return self._resolve_lesser_than(values)

        elif self.relation == self.RELATION_LESSER_THAN_EQUAL:
            return self._resolve_lesser_than_equal(values)

        elif self.relation == self.RELATION_EMPTY:
            return not self._resolve_not_empty(values)

        elif self.relation == self.RELATION_NOT_EMPTY:
            return self._resolve_not_empty(values)

        else:
            return False

    def _resolve_equal(self, values):
        results = []

        for value in values:
            if self.target_option:
                results.append(value.option == self.target_option)
            else:
                results.append(value.text == self.target_text)

        return True in results

    def _resolve_contains(self, values):
        results = []

        for value in values:
            results.append(self.target_text in value.text)

        return True in results

    def _resolve_greater_than(self, values):

        for value in values:
            try:
                if float(value.text) > float(self.target_text):
                    return True
            except ValueError:
                pass

        return False

    def _resolve_greater_than_equal(self, values):

        for value in values:
            try:
                if float(value.text) >= float(self.target_text):
                    return True
            except ValueError:
                pass

        return False

    def _resolve_lesser_than(self, values):

        for value in values:
            try:
                if float(value.text) < float(self.target_text):
                    return True
            except ValueError:
                pass

        return False

    def _resolve_lesser_than_equal(self, values):

        for value in values:
            try:
                if float(value.text) <= float(self.target_text):
                    return True
            except ValueError:
                pass

        return False

    def _resolve_not_empty(self, values):

        for value in values:
            if bool(value.text) or bool(value.option):
                return True

        return False
