import logging
import tempfile
import time
from dataclasses import dataclass, field
from os.path import join as pj
from pathlib import Path
from random import randint
from typing import Callable, Iterable, Optional, Sequence, Tuple

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models

from rest_framework.utils import model_meta

from rdmo.core.utils import get_languages

logger = logging.getLogger(__name__)


ELEMENT_COMMON_FIELDS = (
    'uri_prefix',
    'uri_path',
    'key',
    'comment',
)
IMPORT_INFO_MSG = 'Importing {model} {uri} from {filename}.'


def handle_uploaded_file(filedata):
    tempfilename = generate_tempfile_name()
    with open(tempfilename, 'wb+') as destination:
        for chunk in filedata.chunks():
            destination.write(chunk)
    return tempfilename


def handle_fetched_file(filedata):
    tempfilename = generate_tempfile_name()
    with open(tempfilename, 'wb+') as destination:
        destination.write(filedata)
    return tempfilename


def file_path_exists(file_path):
    return Path(file_path).exists()


def generate_tempfile_name():
    t = int(round(time.time() * 1000))
    r = randint(10000, 99999)
    fn = pj(tempfile.gettempdir(), 'upload_' + str(t) + '_' + str(r) + '.xml')
    return fn


def get_or_return_instance(model: models.Model, uri: Optional[str]=None) -> Tuple[models.Model, bool]:
    if uri is None:
        return model(), True
    try:
        return model.objects.get(uri=uri), False
    except model.DoesNotExist:
        return model(), True


def make_import_info_msg(verbose_name: str, created: bool, uri: Optional[str]=None):
    if uri is None:
        return "%s, no uri" % verbose_name
    if created:
        return f"{verbose_name} created with {uri}"
    return f"{verbose_name} {uri} updated"

@dataclass
class ElementImportHelper:
    model: str
    import_method: Callable
    validators: Iterable[Callable]
    lang_fields: Sequence[str] = field(default_factory=list)
    common_fields: Sequence[str] = field(default=ELEMENT_COMMON_FIELDS)


def get_lang_field_values(field_name: str,
                            element: Optional[dict] = None,
                            instance: models.Model = None,
                            by_field: bool = True):
    if (element and instance):
        raise ValueError("Please choose one of each")

    ret = {}
    for lang_code, _, lang_field in get_languages():
        name_code = f'{field_name}_{lang_code}'
        name_field = f'{field_name}_{lang_field}'
        get_key = name_field if by_field else name_code
        set_key = name_code if by_field else name_field
        if element:
            ret[set_key] = element.get(get_key, '')
        if instance:
            ret[set_key] = getattr(instance, get_key, '')
    return ret

def set_lang_field(instance, field_name, element):
    lang_fields = get_lang_field_values(field_name, element=element)
    for field_lang_name, field_value in lang_fields.items():
        setattr(instance, field_lang_name, field_value)


def set_foreign_field(instance, field_name, element) -> None:
    if field_name not in element:
        return

    foreign_element = element[field_name]

    if not foreign_element:
        setattr(instance, field_name, None)
        return

    foreign_uri = foreign_element.get('uri')

    model_info = model_meta.get_field_info(instance)
    foreign_model = model_info.forward_relations[field_name].related_model

    try:
        foreign_instance = foreign_model.objects.get(uri=foreign_uri)
        setattr(instance, field_name, foreign_instance)
    except foreign_model.DoesNotExist:
        message = '{foreign_model} {foreign_uri} for {instance_model} {instance_uri} does not exist.'.format(
            foreign_model=foreign_model._meta.object_name,
            foreign_uri=foreign_uri,
            instance_model=instance._meta.object_name,
            instance_uri=element.get('uri')
        )
        logger.info(message)
        element['warnings'][foreign_uri].append(message)


def set_m2m_instances(instance, field_name, element):
    if field_name not in element:
        return

    foreign_elements = element.get(field_name, [])

    if not foreign_elements:
        getattr(instance, field_name).clear()
        return

    foreign_instances = []

    model_info = model_meta.get_field_info(instance)
    foreign_model = model_info.forward_relations[field_name].related_model

    for foreign_element in foreign_elements:
        foreign_uri = foreign_element.get('uri')

        try:
            foreign_instance = foreign_model.objects.get(uri=foreign_uri)
            foreign_instances.append(foreign_instance)
        except foreign_model.DoesNotExist:
            message = '{foreign_model} {foreign_uri} for {instance_model} {instance_uri} does not exist.'.format(
                foreign_model=foreign_model._meta.object_name,
                foreign_uri=foreign_uri,
                instance_model=instance._meta.object_name,
                instance_uri=element.get('uri')
            )
            logger.info(message)
            element['warnings'][foreign_uri].append(message)

    getattr(instance, field_name).set(foreign_instances)


def set_m2m_through_instances(instance, field_name, element, source_name, target_name, through_name) -> None:
    if field_name not in element:
        return

    target_elements = element.get(field_name) or []

    model_info = model_meta.get_field_info(instance)
    through_model = model_info.reverse_relations[through_name].related_model
    target_model = model_info.forward_relations[field_name].related_model
    through_instances = list(getattr(instance, through_name).all())

    for target_element in target_elements:
        target_uri = target_element.get('uri')
        order = target_element.get('order')

        try:
            target_instance = target_model.objects.get(uri=target_uri)

            try:
                # look for the item in items
                through_instance = next(filter(lambda item: getattr(item, target_name).uri == target_instance.uri,
                                               through_instances))

                # update order if the item if it changed
                if through_instance.order != order:
                    through_instance.order = order
                    through_instance.save()

                # remove the through_instance from the through_instances list so that it won't get removed
                through_instances.remove(through_instance)
            except StopIteration:
                # create a new item
                through_model(**{
                    source_name: instance,
                    target_name: target_instance,
                    'order': order
                }).save()

        except target_model.DoesNotExist:
            message = '{target_model} {target_uri} for imported {instance_model} {instance_uri} does not exist.'.format(
                target_model=target_model._meta.object_name,
                target_uri=target_uri,
                instance_model=instance._meta.object_name,
                instance_uri=element.get('uri')
            )
            logger.info(message)
            element['warnings'][target_uri].append(message)

    # remove the remainders of the items list
    for through_instance in through_instances:
        if getattr(through_instance, target_name).uri_prefix == instance.uri_prefix:
            through_instance.delete()


def set_reverse_m2m_through_instance(instance, field_name, element, source_name, target_name, through_name) -> None:
    if field_name not in element:
        return

    target_element = element.get(field_name)

    model_info = model_meta.get_field_info(instance)
    through_model = model_info.reverse_relations[through_name].related_model
    through_info = model_meta.get_field_info(through_model)
    target_model = through_info.forward_relations[target_name].related_model

    target_uri = target_element.get('uri')
    order = target_element.get('order')

    try:
        target_instance = target_model.objects.get(uri=target_uri)
        if target_instance.is_locked:
            message = '{target_model} {target_uri} for imported {instance_model} {instance_uri} is locked.'.format(
                target_model=target_model._meta.object_name,
                target_uri=target_uri,
                instance_model=instance._meta.object_name,
                instance_uri=element.get('uri')
            )
            logger.info(message)
            element['errors'].append(message)
        else:
            through_instance, created = through_model.objects.get_or_create(**{
                source_name: instance,
                target_name: target_instance
            })
            through_instance.order = order
            through_instance.save()

    except target_model.DoesNotExist:
        message = '{target_model} {target_uri} for imported {instance_model} {instance_uri} does not exist.'.format(
            target_model=target_model._meta.object_name,
            target_uri=target_uri,
            instance_model=instance._meta.object_name,
            instance_uri=element.get('uri')
        )
        logger.info(message)
        element['warnings'][target_uri].append(message)


def validate_instance(instance, element, *validators):
    exception_message = None
    try:
        instance.full_clean()
        for validator in validators:
            validator(instance if instance.id else None)(vars(instance))
    except ValidationError as e:
        try:
            exception_message = '; '.join(['{}: {}'.format(key, ', '.join(messages))
                                           for key, messages in e.message_dict.items()])
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
            element['errors'].append(message)


def check_permissions(instance: models.Model, element_uri: str, user: models.Model) -> Optional[str]:
    if user is None:
        return

    app_label = instance._meta.app_label
    model_name = instance._meta.model_name

    if instance.id:
        perms = [f'{app_label}.change_{model_name}_object']
    else:
        perms = [f'{app_label}.add_{model_name}_object']

    if not user.has_perms(perms, instance):
        message = f'You have no permissions to import {instance._meta.object_name} {element_uri}.'
        logger.info(message)
        return message
