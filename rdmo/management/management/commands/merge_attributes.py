import logging
from collections import namedtuple
from textwrap import dedent

from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import gettext_lazy as _

from rdmo.conditions.models import Condition
from rdmo.domain.models import Attribute
from rdmo.management.utils import replace_uri_in_template_string
from rdmo.projects.models import Value
from rdmo.questions.models import Page, Question, QuestionSet
from rdmo.tasks.models import Task
from rdmo.views.models import View

logger = logging.getLogger(__name__)


ModelHelper = namedtuple('ModelHelper', ['model', 'lookup_field', 'field_introspection', 'replacement_function'])

REPLACE_ATTRIBUTE_MODEL_HELPERS = [
    ModelHelper(Page, 'attribute', False, None),
    ModelHelper(QuestionSet, 'attribute', False, None),
    ModelHelper(Question, 'attribute', False, None),
    ModelHelper(Condition, 'source', False, None),
    ModelHelper(Task, 'start_attribute', False, None),
    ModelHelper(Task, 'end_attribute', False, None),
    ModelHelper(Value, 'attribute', False, None),
    ModelHelper(View, 'template', True, replace_uri_in_template_string)
]


def get_queryset(model, lookup_field, field_introspection, *_, attribute=None):
    if attribute is None:
        raise ValueError("attribute is required")
    if field_introspection:
        return model.objects.filter(**{f"{lookup_field}__contains": attribute.path})
    return model.objects.filter(**{lookup_field: attribute})


def replace_attribute_on_instance(instance, lookup_field, source, target, field_introspection, replacement_function):
    instance_field = getattr(instance, lookup_field)

    if isinstance(instance_field, Attribute) and instance_field != source:
        raise ValueError("Instance attribute should be equal to the source attribute")
    if not isinstance(instance_field, Attribute) and not field_introspection:
        raise ValueError("When instance field is not an attribute, it should use field introspection")

    if field_introspection:
        replacement_field = replacement_function(instance_field, source, target)
    else:
        replacement_field = target

    setattr(instance, lookup_field, replacement_field)
    return instance


def replace_attribute_on_element_instances(model,
                                           lookup_field,
                                           field_introspection,
                                           replacement_function,
                                           source=None,
                                           target=None,
                                           save=False
                                           ):
    qs = get_queryset(model, lookup_field, field_introspection, attribute=source)
    replaced_attributes = []
    for instance in qs:
        instance = replace_attribute_on_instance(instance, lookup_field, source, target, field_introspection,
                                                 replacement_function)
        if save:
            instance.save()
        replaced_attributes.append({
            'model_name': model._meta.verbose_name_raw,
            'instance': instance,
            'source': source,
            'target': target,
            'saved': save,
            'source_exists': get_queryset(model, lookup_field, field_introspection, attribute=source).exists()
        })
    return replaced_attributes


def get_valid_attribute(attribute, message_name=''):
    if isinstance(attribute, str):
        attribute_uri = attribute
        try:
            attribute = Attribute.objects.get(uri=attribute_uri)
        except Attribute.DoesNotExist as e:
            raise ValueError(f"{message_name} attribute {attribute_uri} does not exist.") from e
        except Attribute.MultipleObjectsReturned as e:
            raise ValueError(f"{message_name} attribute {attribute_uri} returns multiple objects.") from e
    elif not isinstance(attribute, Attribute):
        raise ValueError(f"{message_name} argument should be of type Attribute.")

    return attribute

def make_elements_message(results):
    element_counts = ", ".join([f"{k.capitalize()}({len(v)})" for k, v in results.items() if v])
    if not element_counts or not any(results.values()):
        return "No elements affected."
    return f"Affected elements: {element_counts}"


def make_affected_projects_message(results):
    value_results = results.get(Value._meta.verbose_name_raw, [])
    if not value_results:
        return "No projects affected."
    msg = "Affected Projects:"
    for project in {i['instance'].project for i in value_results}:
        msg += f"\n\tproject={project} (id={project.id})"
    return msg


def make_affected_instances_message(results):
    if not results:
        return ""
    msg = ""
    for k, merger_results in results.items():
        if not merger_results:
            continue
        msg += f"Merger results for model {k.capitalize()} ({len(merger_results)})"
        msg += '\n'
        for result in merger_results:
            msg += dedent(f'''\
                Model={result['model_name']}
                instance={result['instance']}
                source={result['source'].uri}
                source_exists={result['source_exists']}
                target={result['target'].uri}
                saved={result['saved']}
            ''')
            if hasattr(result['instance'], 'project'):
                msg += f"\nproject={result['instance'].project}"
        msg += '\n'
    return msg


def replace_attribute_on_elements(source, target, model_helpers_with_attributes, save):

    if source.get_descendants():
        raise ValueError(f"Source attribute '{source}' with descendants is not supported.")
    if target.get_descendants():
        raise ValueError(f"Target attribute '{target}' with descendants is not supported.")
    if source == target:
        raise ValueError("Source and Target attribute are the same.")

    results = {}
    for model, lookup_field, field_introspection, replacement_function in model_helpers_with_attributes:
        replaced_attributes = replace_attribute_on_element_instances(
            model,
            lookup_field,
            field_introspection,
            replacement_function,
            source=source,
            target=target,
            save=save
        )
        results[model._meta.verbose_name_raw] = replaced_attributes

    if save and all(a['saved'] for i in results.values() for a in i):
        try:
            source.delete()
        except source.DoesNotExist:
            pass
    return results


def main(source, target, save=False):
    return replace_attribute_on_elements(source, target, REPLACE_ATTRIBUTE_MODEL_HELPERS, save)


class Command(BaseCommand):
    help = 'Replace an attribute with another attribute across multiple models'

    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            required=True,
            help='The URI of the source attribute that will be replaced by the target and will be deleted'
        )
        parser.add_argument(
            '--target',
            required=True,
            help='The URI of the target attribute that will be used to replace the source'
        )
        parser.add_argument(
            '--save',
            action='store_true',
            help='''If specified, the changes will be saved and the source attribute will be deleted.\
                    If not specified, the command will do a dry run.'''
        )

    def handle(self, *args, **options):
        source = options['source']
        target = options['target']
        save = options['save']
        verbosity = options.get('verbosity', 1)

        try:
            source = get_valid_attribute(source, message_name='Source')
            target = get_valid_attribute(target, message_name='Target')
            results = main(source, target, save)

            if verbosity >= 1:
                if verbosity >= 2:
                    affected_instances_msg = make_affected_instances_message(results)
                    if affected_instances_msg:
                        self.stdout.write(affected_instances_msg)
                affect_elements_msg = make_elements_message(results)
                affected_projects_msg = make_affected_projects_message(results)
                if save:
                    self.stdout.write(self.style.SUCCESS(
                        f"Successfully replaced source attribute {source.uri} with {target.uri}.\n"
                        f"Source attribute {source.uri} was deleted.\n"
                        f"{affect_elements_msg}\n"
                        f"{affected_projects_msg}"
                    ))
                else:
                    self.stdout.write(self.style.SUCCESS(
                        f"Source attribute {source.uri} can be replaced with {target.uri}.\n"
                        f"{affect_elements_msg}\n"
                        f"{affected_projects_msg}"
                    ))
        except ValueError as e:
            raise CommandError(e) from e
        except Exception as e:
            raise CommandError(_('There was an unknown error in calling the command. %s') % e) from e
