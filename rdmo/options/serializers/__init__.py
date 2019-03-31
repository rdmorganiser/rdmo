from rest_framework import serializers

from rdmo.core.serializers import TranslationSerializerMixin
from rdmo.core.utils import get_language_warning
from rdmo.conditions.models import Condition

from ..models import OptionSet, Option
from ..validators import OptionSetUniqueKeyValidator, OptionUniquePathValidator


class OptionSetIndexOptionsSerializer(serializers.ModelSerializer):

    warning = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = (
            'id',
            'path',
            'text',
            'warning'
        )

    def get_warning(self, obj):
        return get_language_warning(obj, 'text')


class OptionSetIndexSerializer(serializers.ModelSerializer):

    options = OptionSetIndexOptionsSerializer(many=True)

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'key',
            'options'
        )


class OptionSetSerializer(serializers.ModelSerializer):

    key = serializers.CharField(required=True)

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'uri_prefix',
            'key',
            'comment',
            'order',
            'conditions'
        )
        validators = (OptionSetUniqueKeyValidator(),)


class OptionSerializer(TranslationSerializerMixin, serializers.ModelSerializer):

    key = serializers.CharField(required=True)
    optionset = serializers.PrimaryKeyRelatedField(queryset=OptionSet.objects.all(), required=True)

    class Meta:
        model = Option
        fields = (
            'id',
            'optionset',
            'uri_prefix',
            'key',
            'comment',
            'order',
            'additional_input'
        )
        trans_fields = (
            'text',
        )
        validators = (OptionUniquePathValidator(),)


class ConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'key'
        )
