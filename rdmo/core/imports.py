import logging
import tempfile
import time
from os.path import join as pj
from pathlib import Path
from random import randint

from django.core.exceptions import ObjectDoesNotExist, ValidationError

from rest_framework.utils import model_meta

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


def set_common_fields(instance, element):
    instance.uri_prefix = element.get('uri_prefix') or ''
    instance.uri_path = element.get('uri_path') or ''
    instance.key = element.get('key') or ''
    instance.comment = element.get('comment') or ''

    # these are temporary fields for the import only
    # uri is set automatically when saving the instance
    instance.uri = element.get('uri')
    instance.object_name = instance._meta.object_name
    instance.missing = {}
    instance.errors = []


def set_lang_field(instance, field_name, element):
    for lang_code, lang_string, lang_field in get_languages():
        field = element.get('%s_%s' % (field_name, lang_code))
        if field:
            setattr(instance, '%s_%s' % (field_name, lang_field), field)
        else:
            setattr(instance, '%s_%s' % (field_name, lang_field), '')


def set_foreign_field(instance, field_name, element):
    if field_name in element:
        foreign_element = element[field_name]

        if foreign_element:
            uri = foreign_element.get('uri')

            model_info = model_meta.get_field_info(instance)
            foreign_model = model_info.forward_relations[field_name].related_model

            try:
                foreign_instance = foreign_model.objects.get(uri=uri)
                setattr(instance, field_name, foreign_instance)
            except foreign_model.DoesNotExist:
                logger.info('{foreign_model} {foreign_uri} for {instance_model} {instance_uri} does not exist.'.format(
                    foreign_model=foreign_model._meta.object_name,
                    foreign_uri=uri,
                    instance_model=instance._meta.object_name,
                    instance_uri=instance.uri
                ))
                instance.missing[uri] = {
                    'foreign_model': foreign_model._meta.verbose_name,
                    'foreign_uri': uri
                }
        else:
            setattr(instance, field_name, None)


def set_m2m_instances(instance, field_name, element):
    if field_name in element:
        foreign_elements = element.get(field_name, [])

        if foreign_elements:
            foreign_instances = []

            model_info = model_meta.get_field_info(instance)
            foreign_model = model_info.forward_relations[field_name].related_model

            for foreign_element in foreign_elements:
                uri = foreign_element.get('uri')

                try:
                    foreign_instance = foreign_model.objects.get(uri=uri)
                    foreign_instances.append(foreign_instance)
                except foreign_model.DoesNotExist:
                    logger.info('{foreign_model} {foreign_uri} for imported {instance_model} {instance_uri} does not exist.'.format(
                        foreign_model=foreign_model._meta.object_name,
                        foreign_uri=uri,
                        instance_model=instance._meta.object_name,
                        instance_uri=instance.uri
                    ))
                    instance.missing[uri] = {
                        'foreign_model': foreign_model._meta.verbose_name,
                        'foreign_uri': uri
                    }

            getattr(instance, field_name).set(foreign_instances)
        else:
            getattr(instance, field_name).clear()


def set_m2m_through_instances(instance, field_name, element, source_name, target_name, through_name):
    if field_name in element:
        target_elements = element.get(field_name)

        model_info = model_meta.get_field_info(instance)
        through_model = model_info.reverse_relations[through_name].related_model
        target_model = model_info.forward_relations[field_name].related_model
        through_instances = list(getattr(instance, through_name).all())

        if target_elements:
            for target_element in target_elements:
                uri = target_element.get('uri')
                order = target_element.get('order')

                try:
                    target_instance = target_model.objects.get(uri=uri)

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
                    logger.info('{target_model} {target_uri} for imported {instance_model} {instance_uri} does not exist.'.format(
                        target_model=target_model._meta.object_name,
                        target_uri=uri,
                        instance_model=instance._meta.object_name,
                        instance_uri=instance.uri
                    ))
                    instance.missing[uri] = {
                        'target_model': target_model._meta.verbose_name,
                        'target_uri': uri
                    }

        # remove the remainders of the items list
        for through_instance in through_instances:
            if getattr(through_instance, target_name).uri_prefix == instance.uri_prefix:
                through_instance.delete()


def set_reverse_m2m_through_instance(instance, field_name, element, source_name, target_name, through_name):
    if field_name in element:
        target_element = element.get(field_name)

        model_info = model_meta.get_field_info(instance)
        through_model = model_info.reverse_relations[through_name].related_model
        through_info = model_meta.get_field_info(through_model)
        target_model = through_info.forward_relations[target_name].related_model

        uri = target_element.get('uri')
        order = target_element.get('order')

        try:
            target_instance = target_model.objects.get(uri=uri)

            through_instance, created = through_model.objects.get_or_create(**{
                source_name: instance,
                target_name: target_instance
            })
            through_instance.order = order
            through_instance.save()

        except target_model.DoesNotExist:
            logger.info('{target_model} {target_uri} for imported {instance_model} {instance_uri} does not exist.'.format(
                target_model=target_model._meta.object_name,
                target_uri=uri,
                instance_model=instance._meta.object_name,
                instance_uri=instance.uri
            ))
            instance.missing[uri] = {
                'target_model': target_model._meta.verbose_name,
                'target_uri': uri
            }


def validate_instance(instance, *validators):
    exception_message = None
    try:
        for validator in validators:
            data = vars(instance)

            # add foreign keys to parent fields to data
            # for parent_field in getattr(instance, 'parent_fields', []):
            #     data[parent_field] = getattr(instance, parent_field, None)

            # run the validator
            validator(instance if instance.id else None)(data)

    except ValidationError as e:
        try:
            exception_message = '; '.join(['{}: {}'.format(key, ', '.join(messages)) for key, messages in e.message_dict.items()])
        except AttributeError:
            exception_message = ''.join(e.messages)
    except ObjectDoesNotExist as e:
        exception_message = e
    else:
        return True
    finally:
        if exception_message is not None:
            message = '{instance_model} {instance_uri} cannot be imported ({exception}).'.format(
                instance_model=instance._meta.object_name,
                instance_uri=instance.uri,
                exception=exception_message
            )
            logger.info(message)
            instance.errors.append(message)
