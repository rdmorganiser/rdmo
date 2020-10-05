import iso8601
from django.db import models
from django.utils.translation import ugettext_lazy as _

from rdmo.core.constants import (VALUE_TYPE_BOOLEAN, VALUE_TYPE_CHOICES,
                                 VALUE_TYPE_DATETIME, VALUE_TYPE_TEXT)
from rdmo.core.models import Model
from rdmo.domain.models import Attribute
from rdmo.options.models import Option
from rdmo.questions.models import Question

from ..managers import ValueManager


class Value(Model):

    objects = ValueManager()

    FALSE_TEXT = [None, '', '0', 'f', 'F', 'false', 'False']

    project = models.ForeignKey(
        'Project', on_delete=models.CASCADE, related_name='values',
        verbose_name=_('Project'),
        help_text=_('The project this value belongs to.')
    )
    snapshot = models.ForeignKey(
        'Snapshot', blank=True, null=True,
        on_delete=models.CASCADE, related_name='values',
        verbose_name=_('Snapshot'),
        help_text=_('The snapshot this value belongs to.')
    )
    attribute = models.ForeignKey(
        Attribute, blank=True, null=True,
        on_delete=models.SET_NULL, related_name='values',
        verbose_name=_('Attribute'),
        help_text=_('The attribute this value belongs to.')
    )
    set_index = models.IntegerField(
        default=0,
        verbose_name=_('Set index'),
        help_text=_('The position of this value in an entity collection (i.e. in the question set)')
    )
    collection_index = models.IntegerField(
        default=0,
        verbose_name=_('Collection index'),
        help_text=_('The position of this value in an attribute collection.')
    )
    text = models.TextField(
        blank=True,
        verbose_name=_('Text'),
        help_text=_('The string stored for this value.')
    )
    option = models.ForeignKey(
        Option, blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
        verbose_name=_('Option'),
        help_text=_('The option stored for this value.')
    )
    value_type = models.CharField(
        max_length=8, choices=VALUE_TYPE_CHOICES, default=VALUE_TYPE_TEXT,
        verbose_name=_('Value type'),
        help_text=_('Type of this value.')
    )
    unit = models.CharField(
        max_length=64, blank=True,
        verbose_name=_('Unit'),
        help_text=_('Unit for this value.')
    )
    external_id = models.CharField(
        max_length=256, blank=True,
        verbose_name=_('External id'),
        help_text=_('External id for this value.')
    )

    class Meta:
        ordering = ('attribute', 'set_index', 'collection_index' )
        verbose_name = _('Value')
        verbose_name_plural = _('Values')

    # def __str__(self):
    #     if self.attribute:
    #         attribute_label = self.attribute.path
    #     else:
    #         attribute_label = 'none'

    #     if self.snapshot:
    #         snapshot_title = self.snapshot.title
    #     else:
    #         snapshot_title = _('current')

    #     return '%s / %s / %s.%i.%i = "%s"' % (
    #         self.project.title,
    #         snapshot_title,
    #         attribute_label,
    #         self.set_index,
    #         self.collection_index,
    #         self.value
    #     )

    @property
    def value(self):
        if self.option:
            value = self.option.text or ''
            if self.option.additional_input and self.text:
                value += ': ' + self.text
            return value

        elif self.text:
            if self.value_type == VALUE_TYPE_DATETIME:
                try:
                    return iso8601.parse_date(self.text).date()
                except iso8601.ParseError:
                    return self.text
            elif self.value_type == VALUE_TYPE_BOOLEAN:
                if self.text == '1':
                    return _('Yes')
                else:
                    return _('No')
            else:
                return self.text
        else:
            return None

    @property
    def value_and_unit(self):
        value = self.value

        if value is None:
            return ''
        elif self.unit:
            return '%s %s' % (value, self.unit)
        else:
            return value

    @property
    def is_true(self):
        return self.text not in self.FALSE_TEXT

    @property
    def is_false(self):
        return self.text in self.FALSE_TEXT

    @property
    def as_number(self):
        try:
            val = self.text
        except AttributeError:
            return 0
        else:
            if isinstance(val, str):
                val = val.replace(',', '.')
            if isinstance(val, float) is False:
                try:
                    return int(val)
                except ValueError:
                    pass
                try:
                    return float(val)
                except ValueError:
                    return 0
            else:
                return val

    def get_question(self, catalog):
        if self.attribute is not None:
            return Question.objects.filter(questionset__section__catalog=catalog).filter(
                attribute=self.attribute
            ).first()
        else:
            return None

    def get_current_value(self, current_project):
        if (self.attribute is not None) and (current_project is not None):
            return current_project.values.filter(
                snapshot=None,
                attribute=self.attribute,
                set_index=self.set_index,
                collection_index=self.collection_index
            ).first()
        else:
            return None
