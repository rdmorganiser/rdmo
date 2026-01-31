from django.core.exceptions import ValidationError

from rest_framework import serializers


class RDMOException(Exception):
    pass

def raise_as_drf_validation_error(exc: ValidationError) -> None:
    if hasattr(exc, "message_dict"):
        raise serializers.ValidationError(exc.message_dict) from exc

    messages = getattr(exc, "messages", None) or [str(exc)]
    raise serializers.ValidationError({"non_field_errors": messages}) from exc
