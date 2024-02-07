from datetime import timedelta

from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
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
