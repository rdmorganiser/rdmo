from datetime import datetime, timedelta

from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist, ValidationError
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

        if text and settings.PROJECT_VALUES_VALIDATION:
            if value_type == 'url' and settings.PROJECT_VALUES_VALIDATION_URL:
                try:
                    URLValidator()(text)
                except ValidationError as e:
                    raise serializers.ValidationError({
                        'text': [e.message]
                    }) from e

            elif value_type == 'integer' and settings.PROJECT_VALUES_VALIDATION_INTEGER:
                try:
                    RegexValidator(settings.PROJECT_VALUES_VALIDATION_INTEGER_REGEX)(text)
                except ValidationError as e:
                    raise serializers.ValidationError({
                        'text': [settings.PROJECT_VALUES_VALIDATION_INTEGER_MESSAGE]
                    }) from e

            elif value_type == 'float' and settings.PROJECT_VALUES_VALIDATION_FLOAT:
                try:
                    RegexValidator(settings.PROJECT_VALUES_VALIDATION_FLOAT_REGEX)(text)
                except ValidationError as e:
                    raise serializers.ValidationError({
                        'text': [settings.PROJECT_VALUES_VALIDATION_FLOAT_MESSAGE]
                    }) from e

            if value_type == 'boolean' and settings.PROJECT_VALUES_VALIDATION_BOOLEAN:
                try:
                    RegexValidator(settings.PROJECT_VALUES_VALIDATION_BOOLEAN_REGEX)(text)
                except ValidationError as e:
                    raise serializers.ValidationError({
                        'text': [settings.PROJECT_VALUES_VALIDATION_BOOLEAN_MESSAGE]
                    }) from e

            elif value_type == 'date' and settings.PROJECT_VALUES_VALIDATION_DATE:
                try:
                    RegexValidator(settings.PROJECT_VALUES_VALIDATION_DATE_REGEX)(text)
                except ValidationError as e:
                    raise serializers.ValidationError({
                        'text': [settings.PROJECT_VALUES_VALIDATION_DATE_MESSAGE]
                    }) from e

            elif value_type == 'datetime' and settings.PROJECT_VALUES_VALIDATION_DATETIME:
                try:
                    datetime.fromisoformat(text)
                except ValueError as e:
                    raise serializers.ValidationError({
                        'text': [_('Enter a valid datetime.')]
                    }) from e

            elif value_type == 'email' and settings.PROJECT_VALUES_VALIDATION_EMAIL:
                try:
                    EmailValidator()(text)
                except ValidationError as e:
                    raise serializers.ValidationError({
                        'text': [e.message]
                    }) from e

            elif value_type == 'phone' and settings.PROJECT_VALUES_VALIDATION_PHONE:
                try:
                    RegexValidator(settings.PROJECT_VALUES_VALIDATION_PHONE_REGEX)(text)
                except ValidationError as e:
                    raise serializers.ValidationError({
                        'text': [settings.PROJECT_VALUES_VALIDATION_PHONE_MESSAGE]
                    }) from e
