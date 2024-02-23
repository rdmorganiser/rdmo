import logging
import tempfile
import time
from dataclasses import dataclass, field
from os.path import join as pj
from pathlib import Path
from random import randint
from typing import Callable, Dict, Iterable, Optional, Sequence, Tuple

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from rest_framework.utils import model_meta

from rdmo.core.constants import ELEMENT_COMMON_FIELDS, ELEMENT_IMPORT_EXTRA_FIELDS_DEFAULTS
from rdmo.core.utils import get_languages

logger = logging.getLogger(__name__)


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


def get_or_return_instance(model: Callable, uri: Optional[str]=None) -> Tuple[models.Model, bool]:
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

@dataclass(frozen=True)
class ElementImportHelper:
    model: Optional[models.Model] = field(default=None)
    model_path: Optional[str] = field(default=None)
    validators: Iterable[Callable] = field(default_factory=list)
    serializer: Optional[Callable] = field(default=None)
    common_fields: Sequence[str] = field(default=ELEMENT_COMMON_FIELDS)
    lang_fields: Sequence[str] = field(default_factory=list)
    foreign_fields: Sequence[str] = field(default_factory=list)
    extra_fields: Sequence[str] = field(default_factory=list)
    m2m_instance_fields: Sequence[str] = field(default_factory=list)
    m2m_through_instance_fields: Sequence[Dict[str, str]] = field(default_factory=list)
    reverse_m2m_through_instance_fields: Sequence[Dict[str, str]] = field(default_factory=list)
    add_current_site_editors: bool = field(default=True)
    add_current_site_sites: bool = field(default=False)


def get_lang_field_values(field_name: str,
                        element: Optional[dict] = None,
                        instance: Optional[models.Model] = None,
                        get_by_lang_field_key: bool = True):
    if (element is not None and instance is not None):
        raise ValueError("Please choose one of each")

    ret = []
    for lang_code, lang_verbose_name, lang_field in get_languages():
        name_code = f'{field_name}_{lang_code}'
        name_field = f'{field_name}_{lang_field}'
        # get_key = name_field if get_by_lang_field_key else name_code
        # set_key = name_code if get_by_lang_field_key else name_field
        row = {}
        row['element_key'] = name_code
        row['instance_field'] = name_field
        if element:
            row['value'] = element.get(name_code, '') or ''
        if instance:
            row['value'] = getattr(instance, name_field, '') or ''
        ret.append(row)
    return ret

def set_lang_field(instance, field_name, element):
    languages_field_values = get_lang_field_values(field_name, element=element)
    for lang_fields_value in languages_field_values:
        field_lang_name = lang_fields_value['instance_field']
        field_value = lang_fields_value['value']

        setattr(instance, field_lang_name, field_value)


def set_foreign_field(instance, field_name, element, uploaded_uris=None) -> None:
    if field_name not in element:
        return

    foreign_element = element[field_name]

    if not foreign_element:
        setattr(instance, field_name, None)
        return

    if 'uri' not in foreign_element:
        message = 'Foreign model can not be assigned on {instance_model}.{field_name} {instance_uri} due to missing uri.'.format( # noqa: E501
            instance_model=instance._meta.object_name,
            instance_uri=element.get('uri'),
            field_name=field_name
        )
        logger.info(message)
        element['errors'][element.get('uri')].append(message)
        return

    foreign_uri = foreign_element['uri']

    model_info = model_meta.get_field_info(instance)
    foreign_model = model_info.forward_relations[field_name].related_model
    foreign_instance = None
    try:
        foreign_instance = foreign_model.objects.get(uri=foreign_uri)
    except foreign_model.DoesNotExist:
        message = '{foreign_model} {foreign_uri} for {instance_model} {instance_uri} does not exist.'.format(
            foreign_model=foreign_model._meta.object_name,
            foreign_uri=foreign_uri,
            instance_model=instance._meta.object_name,
            instance_uri=element.get('uri')
        )
        logger.info(message)
        element['warnings'][foreign_uri].append(message)
    try:
        if foreign_instance is not None:
            setattr(instance, field_name, foreign_instance)
    except ValueError:
        message = '{foreign_model} {foreign_uri} can not be assigned on {instance_model}.{field_name} {instance_uri} .'.format( # noqa: E501
            foreign_model=foreign_model._meta.object_name,
            foreign_uri=foreign_uri,
            instance_model=instance._meta.object_name,
            instance_uri=element.get('uri'),
            field_name=field_name,
            )
        logger.info(message)
        element['errors'][foreign_uri].append(message)



def set_extra_field(instance, field_name, element, questions_widget_types=None) -> None:

    element_value = element.get(field_name)
    default_value = ELEMENT_IMPORT_EXTRA_FIELDS_DEFAULTS.get(field_name)
    extra_value = element_value or default_value
    if field_name == 'widget_type':
        if element_value in questions_widget_types:
            extra_value = element_value
        else:
            extra_value = default_value
    if field_name == "path":
        if instance.key and hasattr(instance, "build_path"):
            extra_value = instance.build_path(instance.key, instance.parent)
        else:
            exception_message = _('This field may not be blank.')
            message = '{instance_model} {instance_uri} cannot be imported (key: {exception}) .'.format(
                instance_model=instance._meta.object_name,
                instance_uri=element.get('uri'),
                exception=exception_message
            )
            logger.info(message)
            element['errors'].append(message)

    setattr(instance, field_name, extra_value)


def set_m2m_instances(instance, element, field_name):
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


def set_m2m_through_instances(instance, element, field_name=None, source_name=None,
                              target_name=None, through_name=None) -> None:
    if field_name not in element:
        return
    if not all([source_name, target_name, through_name]):
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


def set_reverse_m2m_through_instance(instance, element, field_name=None, source_name=None,
                                     target_name=None, through_name=None) -> None:
    if field_name not in element:
        return
    if not all([source_name, target_name, through_name]):
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
        message = _('You have no permissions to import') + f'{instance._meta.object_name} {element_uri}.'
        logger.info(message)
        return message
