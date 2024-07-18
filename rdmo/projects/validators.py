from datetime import datetime, timedelta

from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist, ValidationError
from django.core.validators import EmailValidator, RegexValidator, URLValidator
from django.utils.dateparse import parse_datetime
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from rdmo.core.constants import (
    VALUE_TYPE_BOOLEAN,
    VALUE_TYPE_DATE,
    VALUE_TYPE_DATETIME,
    VALUE_TYPE_EMAIL,
    VALUE_TYPE_FILE,
    VALUE_TYPE_FLOAT,
    VALUE_TYPE_INTEGER,
    VALUE_TYPE_PHONE,
    VALUE_TYPE_URL,
)
from rdmo.core.utils import human2bytes


class ValueConflictValidator:

    requires_context = True

    def __call__(self, data, serializer):
        if serializer.instance:
            # for an update, check if the value was updated in the meantime
            updated = serializer.context['view'].request.data.get('updated')

            if updated is not None:
                delta = abs(parse_datetime(updated) - serializer.instance.updated)
                if delta > timedelta(seconds=settings.PROJECT_VALUES_CONFLICT_THRESHOLD):
                    raise serializers.ValidationError({
                        'conflict': [_('A newer version of this value was found.')]
                    })
        else:
            # for a new value, check if there is already a value with the same attribute and indexes
            get_kwargs = {
                'attribute': data.get('attribute'),
                'set_prefix': data.get('set_prefix'),
                'set_index': data.get('set_index'),
                'collection_index': data.get('collection_index')
            }

            # for checkboxes, check only values with the same option. the widget_type is provided with the post request
            widget_type = serializer.context['view'].request.data.get('widget_type')
            if widget_type == 'checkbox':
                get_kwargs['option'] = data.get('option')

            try:
                serializer.context['view'].project.values.filter(snapshot=None).get(**get_kwargs)
            except ObjectDoesNotExist:
                return
            except MultipleObjectsReturned:
                pass

            raise serializers.ValidationError({
                'conflict': [_('An existing value for this attribute/set_prefix/set_index/collection_index'
                              ' was found.')]
            })


class ValueQuotaValidator:

    requires_context = True

    def __call__(self, data, serializer):
        if serializer.context['view'].action == 'create' and data.get('value_type') == VALUE_TYPE_FILE:
            project = serializer.context['view'].project
            if project.file_size > human2bytes(settings.PROJECT_FILE_QUOTA):
                raise serializers.ValidationError({
                    'quota': [_('The file quota for this project has been reached.')]
                })


class ValueTypeValidator:

    def __call__(self, data):
        text = data.get('text')
        value_type = data.get('value_type')

        try:
            self.validate(text, value_type)
        except ValidationError as e:
            raise serializers.ValidationError({
                'text': [e.message]
            }) from e

    def validate(self, text, value_type):
        if text and settings.PROJECT_VALUES_VALIDATION:
            if value_type == VALUE_TYPE_URL and settings.PROJECT_VALUES_VALIDATION_URL:
                URLValidator()(text)

            elif value_type == VALUE_TYPE_INTEGER and settings.PROJECT_VALUES_VALIDATION_INTEGER:
                RegexValidator(
                    settings.PROJECT_VALUES_VALIDATION_INTEGER_REGEX,
                    settings.PROJECT_VALUES_VALIDATION_INTEGER_MESSAGE
                )(text)

            elif value_type == VALUE_TYPE_FLOAT and settings.PROJECT_VALUES_VALIDATION_FLOAT:
                RegexValidator(
                    settings.PROJECT_VALUES_VALIDATION_FLOAT_REGEX,
                    settings.PROJECT_VALUES_VALIDATION_FLOAT_MESSAGE
                )(text)

            elif value_type == VALUE_TYPE_BOOLEAN and settings.PROJECT_VALUES_VALIDATION_BOOLEAN:
                RegexValidator(
                    settings.PROJECT_VALUES_VALIDATION_BOOLEAN_REGEX,
                    settings.PROJECT_VALUES_VALIDATION_BOOLEAN_MESSAGE
                )(text)

            elif value_type == VALUE_TYPE_DATE and settings.PROJECT_VALUES_VALIDATION_DATE:
                RegexValidator(
                    settings.PROJECT_VALUES_VALIDATION_DATE_REGEX,
                    settings.PROJECT_VALUES_VALIDATION_DATE_MESSAGE
                )(text)

            elif value_type == VALUE_TYPE_DATETIME and settings.PROJECT_VALUES_VALIDATION_DATETIME:
                try:
                    datetime.fromisoformat(text)
                except ValueError as e:
                    raise ValidationError(_('Enter a valid datetime.')) from e

            elif value_type == VALUE_TYPE_EMAIL and settings.PROJECT_VALUES_VALIDATION_EMAIL:
                EmailValidator()(text)

            elif value_type == VALUE_TYPE_PHONE and settings.PROJECT_VALUES_VALIDATION_PHONE:
                RegexValidator(
                    settings.PROJECT_VALUES_VALIDATION_PHONE_REGEX,
                    settings.PROJECT_VALUES_VALIDATION_PHONE_MESSAGE
                )(text)
