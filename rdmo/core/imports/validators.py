import logging

from django.core.exceptions import ObjectDoesNotExist, ValidationError

from rdmo.core.imports.element_changes import ImportElementFields
from rdmo.core.imports.element_messages import track_messages_on_element
from rdmo.core.validators import LockedValidator

logger = logging.getLogger(__name__)

def format_message_from_validation_error(exception: ValidationError) -> str:
    message = '; '.join(['{}: {}'.format(key, ', '.join(messages)) for key, messages in exception.message_dict.items()])
    return message


def validate_instance(instance, element, *validators):
    exception_message = None
    try:
        instance.full_clean()
    except ValidationError as e:
        exception_message = format_message_from_validation_error(e)
        message = '{instance_model} {instance_uri} cannot be imported ({exception}).'.format(
            instance_model=instance._meta.object_name,
            instance_uri=element.get('uri'),
            exception=exception_message
        )
        logger.info(message)
        _key = "FullClean"
        element[ImportElementFields.ERRORS].append(message)
        track_messages_on_element(element, _key, error=message)
        return

    for validator in validators:
        if issubclass(validator, LockedValidator):
            element['locked'] = False
        try:
            validator(instance=instance if instance.id else None)(vars(instance))
        except ValidationError as e:
            try:
                exception_message = format_message_from_validation_error(e)
            except AttributeError:
                exception_message = ''.join(e.messages)
        except ObjectDoesNotExist as e:
            exception_message = e
        finally:
            if exception_message is not None:
                message = '{instance_model} {instance_uri} cannot be imported ({exception}).'.format(
                    instance_model=instance._meta.object_name,
                    instance_uri=element.get('uri'),
                    exception=exception_message
                )
                logger.info(message)
                _key = validator.__qualname__
                element[ImportElementFields.ERRORS].append(message)
                track_messages_on_element(element, _key, error=message)
                if issubclass(validator, LockedValidator):
                    element['locked'] = True
