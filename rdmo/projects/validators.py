from datetime import datetime, timedelta

from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.validators import EmailValidator, RegexValidator, URLValidator
from django.utils.dateparse import parse_datetime
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from rdmo.core.constants import VALUE_TYPE_FILE
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
            try:
                serializer.context['view'].project.values.filter(snapshot=None).get(
                    attribute=data.get('attribute'),
                    set_prefix=data.get('set_prefix'),
                    set_index=data.get('set_index'),
                    collection_index=data.get('collection_index')
                )
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

    requires_context = True

    def __call__(self, data, serializer):
        text = data.get('text')
        value_type = data.get('value_type')

        if text is not None:
            if value_type == 'url' and settings.PROJECT_VALUES_URL_VALIDATION:
                URLValidator()(text)

            elif value_type == 'integer' and settings.PROJECT_VALUES_INTEGER_VALIDATION:
                RegexValidator(
                    settings.PROJECT_VALUES_INTEGER_VALIDATION_REGEX,
                    settings.PROJECT_VALUES_INTEGER_VALIDATION_MESSAGE
                )(text)

            elif value_type == 'float' and settings.PROJECT_VALUES_FLOAT_VALIDATION:
                RegexValidator(
                    settings.PROJECT_VALUES_FLOAT_VALIDATION_REGEX,
                    settings.PROJECT_VALUES_FLOAT_VALIDATION_MESSAGE
                )(text)

            if value_type == 'boolean' and settings.PROJECT_VALUES_BOOLEAN_VALIDATION:
                RegexValidator(
                    settings.PROJECT_VALUES_BOOLEAN_VALIDATION_REGEX,
                    settings.PROJECT_VALUES_BOOLEAN_VALIDATION_MESSAGE
                )(text)

            elif value_type == 'date' and settings.PROJECT_VALUES_DATE_VALIDATION:
                RegexValidator(
                    settings.PROJECT_VALUES_DATE_VALIDATION_REGEX,
                    settings.PROJECT_VALUES_DATE_VALIDATION_MESSAGE
                )(text)

            elif value_type == 'datetime' and settings.PROJECT_VALUES_DATETIME_VALIDATION:
                try:
                    datetime.fromisoformat(text)
                except ValueError as e:
                    raise serializers.ValidationError({
                        'text': [_('Enter a valid datetime.')]
                    }) from e

            elif value_type == 'email' and settings.PROJECT_VALUES_EMAIL_VALIDATION:
                EmailValidator()(text)

            elif value_type == 'phone' and settings.PROJECT_VALUES_PHONE_VALIDATION:
                RegexValidator(
                    settings.PROJECT_VALUES_PHONE_VALIDATION_REGEX,
                    settings.PROJECT_VALUES_PHONE_VALIDATION_MESSAGE
                )(text)
