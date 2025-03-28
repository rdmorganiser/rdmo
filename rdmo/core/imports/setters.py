import logging
from typing import Optional

from rest_framework.utils import model_meta

from rdmo.core.imports.element_changes import (
    ImportElementFields,
    track_changes_m2m_instances,
    track_changes_on_element,
    track_changes_on_m2m_through_instances,
    track_changes_on_uri_of_foreign_field,
)
from rdmo.core.imports.element_messages import track_messages_on_element
from rdmo.core.imports.getters import get_lang_field_values, get_rdmo_model_path
from rdmo.core.imports.helpers import ExtraFieldHelper

logger = logging.getLogger(__name__)


def set_common_fields(instance, field_name, element, original=None):
    element_value = element.get(field_name) or ''
    if field_name == 'comment' and original is not None:
        # prevent overwrite with an empty comment when updating an element
        original_value = getattr(original, field_name)
        if original_value and not element_value:
            element_value = original_value
            element[field_name] = element_value

    setattr(instance, field_name, element_value)
    # track changes for common fields
    track_changes_on_element(element, field_name, new_value=element_value, original=original)


def set_lang_field(instance, field_name, element, original=None):
    languages_field_values = get_lang_field_values(field_name, element=element)
    for lang_fields_value in languages_field_values:
        field_lang_name = lang_fields_value['instance_field']
        field_value = lang_fields_value['value']
        element_field = lang_fields_value['element_key']

        track_changes_on_element(element, element_field,
                                 new_value=field_value,
                                 instance_field=field_lang_name,
                                 original=original)
        setattr(instance, field_lang_name, field_value)


def set_foreign_field(instance, field_name, element, original=None) -> None:
    if field_name not in element:
        return

    foreign_element = element[field_name]

    if not foreign_element:
        setattr(instance, field_name, None)
        return

    if 'uri' not in foreign_element:
        message = 'Foreign model can not be assigned on {instance_model}.{field_name} {instance_uri} due to missing uri.'.format(  # noqa: E501
            instance_model=instance._meta.object_name,
            instance_uri=element.get('uri'),
            field_name=field_name
        )
        logger.info(message)
        element[ImportElementFields.ERRORS].append(message)  # errors is a list
        track_messages_on_element(element, field_name, error=message)
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
        element[ImportElementFields.WARNINGS][foreign_uri].append(message)
        track_messages_on_element(element, field_name, warning=message)
    except foreign_model.MultipleObjectsReturned:
        message = '{foreign_model} {foreign_uri} for {instance_model} {instance_uri} returns multiple objects.'.format(
            foreign_model=foreign_model._meta.object_name,
            foreign_uri=foreign_uri,
            instance_model=instance._meta.object_name,
            instance_uri=element.get('uri')
        )
        logger.info(message)
        element[ImportElementFields.WARNINGS][foreign_uri].append(message)
        track_messages_on_element(element, field_name, warning=message)


    try:
        if foreign_instance is not None:
            setattr(instance, field_name, foreign_instance)
        _foreign_uri = foreign_uri if foreign_instance is not None else ""
        track_changes_on_uri_of_foreign_field(element,
                                              field_name,
                                              _foreign_uri,
                                              original=original)
    except ValueError:
        message = '{foreign_model} {foreign_uri} can not be assigned on {instance_model}.{field_name} {instance_uri} .'.format(  # noqa: E501
            foreign_model=foreign_model._meta.object_name,
            foreign_uri=foreign_uri,
            instance_model=instance._meta.object_name,
            instance_uri=element.get('uri'),
            field_name=field_name,
        )
        logger.info(message)
        element[ImportElementFields.ERRORS].append(message)
        track_messages_on_element(element, field_name, error=message)


def set_extra_field(instance, field_name, element,
                    extra_field_helper: Optional[ExtraFieldHelper] = None,
                    ) -> None:

    extra_field_value = None
    if field_name in element:
        extra_field_value = element.get(field_name)
    else:
        # get the default field value from the instance
        instance_value = getattr(instance, field_name)
        element[field_name] = instance_value
        extra_field_value = instance_value

    if extra_field_helper is not None:
        # default_value
        extra_value_from_helper = extra_field_helper.get_value(instance=instance,
                                                   key=field_name)
        # overwrite None or '' values by the get_value from the helper
        if extra_field_value is None or extra_field_value == '':
            extra_field_value = extra_value_from_helper

        if extra_field_helper.overwrite_in_element:
            element[field_name] = extra_field_value

    if extra_field_value is not None:
        setattr(instance, field_name, extra_field_value)


def set_m2m_through_instances(instance, element, field_name=None, source_name=None,
                              target_name=None, through_name=None,
                              original=None, save=None) -> None:
    if field_name not in element:
        return
    if not all([source_name, target_name, through_name]):
        return

    target_elements = element.get(field_name) or []
    if isinstance(target_elements, str):
        target_elements = [target_elements]

    model_info = model_meta.get_field_info(instance)
    through_model = model_info.reverse_relations[through_name].related_model
    target_model = model_info.forward_relations[field_name].related_model
    through_instances = list(getattr(instance, through_name).all())

    new_data = []
    current_data = []

    # get the original data in correct order
    if original is not None:
        try:
            for orig_field_instance in getattr(original, through_name).order_by():
                current_data.append({
                    'uri': getattr(orig_field_instance, target_name).uri,
                    'order': orig_field_instance.order,
                    'model': get_rdmo_model_path(target_name, field_name)
                })
            current_data = sorted(current_data, key=lambda k: k['order'])
        except AttributeError:
            pass  # legacy elements miss the field_name

    for target_element in target_elements:
        target_uri = target_element.get('uri')
        target_element['order'] = int(target_element['order']) # cast to int for ordering
        order = target_element.get('order')
        new_data.append(target_element)

        try:
            target_instance = target_model.objects.get(uri=target_uri)

            try:
                # look for the item in items
                through_instance = next(filter(lambda item: getattr(item, target_name).uri == target_instance.uri,
                                               through_instances))

                # update order of the item when it was changed
                if through_instance.order != order and save:
                    through_instance.order = order
                    through_instance.save()
                if save:
                    # remove the through_instance from the through_instances list so that it won't get removed
                    through_instances.remove(through_instance)
            except StopIteration:
                # create a new item
                if save:
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
            element[ImportElementFields.WARNINGS][target_uri].append(message)
            element[ImportElementFields.WARNINGS][element.get('uri')].append(message)
            track_messages_on_element(element, field_name, warning=message)
        except target_model.MultipleObjectsReturned:
            message = '{target_model} {target_uri} for imported {instance_model} {instance_uri} returns multiple objects.'.format(  # noqa: E501
                target_model=target_model._meta.object_name,
                target_uri=target_uri,
                instance_model=instance._meta.object_name,
                instance_uri=element.get('uri')
            )
            logger.info(message)
            element[ImportElementFields.WARNINGS][target_uri].append(message)
            element[ImportElementFields.WARNINGS][element.get('uri')].append(message)
            track_messages_on_element(element, field_name, warning=message)
    if save:
        # remove the remainders of the items list
        for through_instance in through_instances:
            if getattr(through_instance, target_name).uri_prefix == instance.uri_prefix:
                through_instance.delete()
    # sort the tracked changes by order in-place
    new_data = sorted(new_data, key=lambda k: k['order'])

    track_changes_on_m2m_through_instances(element, field_name, current_data, new_data)


def set_m2m_instances(instance, element, field_name, original=None, save=None):
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
            element[ImportElementFields.WARNINGS][foreign_uri].append(message)
            element[ImportElementFields.WARNINGS][element.get('uri')].append(message)
            track_messages_on_element(element, field_name, warning=message)
    if save:
        getattr(instance, field_name).set(foreign_instances)
    track_changes_m2m_instances(element, field_name,
                                foreign_instances, original=original)


def set_reverse_m2m_through_instance(instance, element, field_name=None, source_name=None,
                                     target_name=None, through_name=None,
                                     original=None, save=None) -> None:
    if field_name not in element:
        return
    if not all([source_name, target_name, through_name]):
        return
    target_elements = element.get(field_name) or []
    if isinstance(target_elements, str):
        target_elements = [target_elements]
    elif isinstance(target_elements, dict):
        target_elements = [target_elements]

    model_info = model_meta.get_field_info(instance)
    through_model = model_info.reverse_relations[through_name].related_model
    through_info = model_meta.get_field_info(through_model)
    target_model = through_info.forward_relations[target_name].related_model

    new_data = []
    current_data = []

    if original is not None:
        try:
            current_data = []
            for _through_instance in getattr(original, through_name).order_by():
                current_data.append({
                    'uri': getattr(_through_instance, source_name).uri,
                    'order': _through_instance.order,
                    'model': get_rdmo_model_path(target_name, field_name),
                })
            current_data = sorted(current_data, key=lambda k: k['order'])
        except AttributeError:
            pass  # legacy elements miss the field_name

    for target_element in target_elements:
        target_uri = target_element.get('uri')
        target_element['order'] = int(target_element['order'])  # cast to int for ordering
        order = target_element.get('order')
        new_data.append(target_element)

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
                element[ImportElementFields.ERRORS].append(message)
                track_messages_on_element(element, field_name, error=message)
                continue
            if save:
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
            element[ImportElementFields.WARNINGS][target_uri].append(message)
            element[ImportElementFields.WARNINGS][element.get('uri')].append(message)
            track_messages_on_element(element, field_name, warning=message)
    # sort the tracked changes by order in-place
    new_data = sorted(new_data, key=lambda k: k['order'])

    track_changes_on_m2m_through_instances(element, field_name, current_data, new_data)
