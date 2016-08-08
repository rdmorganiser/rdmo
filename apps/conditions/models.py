from __future__ import unicode_literals

from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

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
    RELATION_CHOICES = (
        (RELATION_EQUAL, 'is equal to (==)'),
        (RELATION_NOT_EQUAL, 'is not equal to (!=)'),
        (RELATION_CONTAINS, 'contains'),
        (RELATION_GREATER_THAN, 'is greater than (>)'),
        (RELATION_GREATER_THAN_EQUAL, 'is greater than or equal (>=)'),
        (RELATION_LESSER_THAN, 'is lesser than (<)'),
        (RELATION_LESSER_THAN_EQUAL, 'is lesser than or equal (<=)'),
    )

    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)

    source = models.ForeignKey('domain.Attribute', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')
    relation = models.CharField(max_length=8, choices=RELATION_CHOICES)

    target_text = models.CharField(max_length=256, blank=True, null=True)
    target_option = models.ForeignKey('domain.Option', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    class Meta:
        verbose_name = _('Condition')
        verbose_name_plural = _('Conditions')

    def __str__(self):
        return self.title

    def resolve(self, snapshot):
        values = snapshot.values.filter(attribute=self.source)

        results = []
        for value in values:
            if self.relation == self.RELATION_EQUAL:
                if self.target_option:
                    results.append(value.option == self.target_option)
                else:
                    results.append(value.text == self.target_text)

        return True in results
