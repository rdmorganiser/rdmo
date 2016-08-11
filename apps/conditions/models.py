from __future__ import unicode_literals

from django.db import models

from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
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

    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)

    source = models.ForeignKey('domain.Attribute', db_constraint=False, blank=True, null=True, on_delete=models.SET_NULL, related_name='+')
    relation = models.CharField(max_length=8, choices=RELATION_CHOICES)

    target_text = models.CharField(max_length=256, blank=True, null=True)
    target_option = models.ForeignKey('domain.Option', db_constraint=False, blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    class Meta:
        verbose_name = _('Condition')
        verbose_name_plural = _('Conditions')

    def __str__(self):
        return self.title

    def resolve(self, snapshot):
        values = snapshot.values.filter(attribute=self.source)

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
            if self.source.value_type in ('text', 'url'):
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
