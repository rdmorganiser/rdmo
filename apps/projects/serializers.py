from rest_framework.serializers import ModelSerializer

from .models import *


class ValueSerializer(ModelSerializer):

    class Meta:
        model = Value


class ValueSetSerializer(ModelSerializer):

    class Meta:
        model = ValueSet
