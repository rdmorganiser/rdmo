import logging
import tempfile
import time
from os.path import join as pj
from random import randint

from django.core.exceptions import ValidationError

from rdmo.core.utils import get_languages

logger = logging.getLogger(__name__)


def handle_uploaded_file(filedata):
    tempfilename = generate_tempfile_name()
    with open(tempfilename, 'wb+') as destination:
        for chunk in filedata.chunks():
            destination.write(chunk)
    return tempfilename


def generate_tempfile_name():
    t = int(round(time.time() * 1000))
    r = randint(10000, 99999)
    fn = pj(tempfile.gettempdir(), 'upload_' + str(t) + '_' + str(r) + '.xml')
    return fn


def get_instance(element, model):
    try:
        return model.objects.get(uri=element.get('uri'))
    except model.DoesNotExist:
        return model()


def set_common_fields(instance, element):
    instance.uri_prefix = element.get('uri_prefix') or ''
    instance.key = element.get('key') or ''
    instance.comment = element.get('comment') or ''


def set_temporary_fields(instance, element):
    instance.object_name = instance._meta.object_name
    instance.uri = element.get('uri')
    instance.missing = {}
    instance.errors = []


def set_lang_field(instance, field_name, element):
    for lang_code, lang_string, lang_field in get_languages():
        field = element.get('%s_%s' % (field_name, lang_code))
        if field:
            setattr(instance, '%s_%s' % (field_name, lang_field), field)


def set_foreign_field(instance, field_name, element, foreign_model):
    foreign_uri = element.get(field_name)
    if foreign_uri:
        try:
            foreign_field = foreign_model.objects.get(uri=foreign_uri)
            setattr(instance, field_name, foreign_field)
        except foreign_model.DoesNotExist:
            logger.info('{foreign_model} {foreign_uri} for {instance_model} {instance_uri} does not exist.'.format(
                foreign_model=foreign_model._meta.object_name,
                foreign_uri=foreign_uri,
                instance_model=instance._meta.object_name,
                instance_uri=instance.uri
            ))
            instance.missing[foreign_uri] = {
                'foreign_model': foreign_model._meta.verbose_name,
                'foreign_uri': foreign_uri
            }


def get_m2m_instances(instance, field_name, element, foreign_model):
    foreign_instances = []

    foreign_uris = element.get(field_name)
    if foreign_uris:
        for foreign_uri in foreign_uris:
            try:
                foreign_instance = foreign_model.objects.get(uri=foreign_uri)
                foreign_instances.append(foreign_instance)
            except foreign_model.DoesNotExist:
                logger.info('{foreign_model} {foreign_uri} for imported {instance_model} {instance_uri} does not exist.'.format(
                    foreign_model=foreign_model._meta.object_name,
                    foreign_uri=foreign_uri,
                    instance_model=instance._meta.object_name,
                    instance_uri=instance.uri
                ))
                instance.missing[foreign_uri] = {
                    'foreign_model': foreign_model._meta.verbose_name,
                    'foreign_uri': foreign_uri
                }

    return foreign_instances


def validate_instance(instance, validator_model):
    try:
        validator_model(instance).validate()
    except ValidationError as e:
        message = '{instance_model} {instance_uri} cannot be imported ({exception}).'.format(
            instance_model=instance._meta.object_name,
            instance_uri=instance.uri,
            exception=e
        )
        logger.info(message)
        instance.errors.append(message)
