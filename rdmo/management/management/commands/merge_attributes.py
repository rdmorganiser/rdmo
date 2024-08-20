import logging
from textwrap import dedent

from django.core.management.base import BaseCommand, CommandError

from rdmo.domain.models import Attribute
from rdmo.management.utils import replace_uri_in_template_string
from rdmo.projects.models import Value
from rdmo.views.models import View

logger = logging.getLogger(__name__)


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
            default=False,
            help='''If specified, the changes will be saved.\
                    If not specified, the command will not make any changes in the database.'''
            )
        parser.add_argument(
            '--delete',
            action='store_true',
            default=False,
            help='''If specified, the source attribute will be deleted.\
                    If not specified, the command will not delete the source attribute.'''
            )
        parser.add_argument(
            '--view',
            action='store_true',
            default=False,
            help='If specified, the changes will be applied to the affected Views as well.'
        )

    def handle(self, *args, **options):
        source = options['source']
        target = options['target']
        save_changes = options['save']
        delete_source = options['delete']
        update_views = options['view']
        verbosity = options.get('verbosity', 1)

        source = get_valid_attribute(source, message_name='Source')
        target = get_valid_attribute(target, message_name='Target', allow_descendants=True)

        if source == target:
            raise CommandError("Source and Target attribute are the same, nothing to do.")

        results = {}
        related_model_fields = [i for i in Attribute._meta.get_fields()
                                if i.is_relation and not i.many_to_many
                                and i.related_model is not Attribute]

        for related_field in related_model_fields:
            replaced_model_result = replace_attribute_on_related_model_instances(related_field, source=source,
                                                                                 target=target,
                                                                                 save_changes=save_changes)
            results[related_field.related_model._meta.verbose_name_raw] = replaced_model_result

        view_template_result = replace_attribute_in_view_template(source=source, target=target,
                                                                  save_changes=save_changes, update_views=update_views)
        results[View._meta.verbose_name_raw] = view_template_result

        if delete_source:
            try:
                source.delete()
                logger.info("Source attribute %s was deleted.", source.uri)
            except source.DoesNotExist:
                logger.info("Source attribute %s did not exist.", source.uri)

        if verbosity >= 1:
            all_instances_were_updated = all(a['saved'] for i in results.values() for a in i)
            affect_elements_msg = make_affected_elements_counts_message(results)
            affected_projects_msg = make_affected_projects_message(results)
            affected_views_msg = make_affected_views_message(results)
            if save_changes:
                info_msg = f"Successfully replaced source attribute {source.uri} with {target.uri} on affected elements."  # noqa: E501
                if update_views:
                    info_msg += f"\nSuccessfully replaced source attribute {source.uri} in affected View templates."
                self.stdout.write(self.style.SUCCESS(info_msg))

            if delete_source:
                self.stdout.write(self.style.SUCCESS(
                    f"Source attribute {source.uri} was deleted.\n"
                ))
                if not all_instances_were_updated:
                    self.stdout.write(
                        self.style.NOTICE(f"Source attribute {source.uri} was deleted without moving affected elements to the target attribute.")  # noqa: E501
                    )
            if not save_changes and not delete_source:
                self.stdout.write(self.style.SUCCESS(
                    f"Nothing was changed. Displaying affected elements for replacement of source attribute {source.uri} with target {target.uri}."  # noqa: E501
                ))

            self.stdout.write(self.style.SUCCESS(
                f"{affect_elements_msg}\n"
                f"{affected_projects_msg}\n"
                f"{affected_views_msg}"
            ))

            if verbosity >= 2:
                affected_instances_msg = make_affected_instances_detail_message(results)
                self.stdout.write()
                self.stdout.write(affected_instances_msg)


def get_attribute_from_uri(attribute_uri, message_name=''):
    try:
        attribute = Attribute.objects.get(uri=attribute_uri)
        return attribute
    except Attribute.DoesNotExist as e:
        raise CommandError(f"{message_name} attribute {attribute_uri} does not exist.") from e
    except Attribute.MultipleObjectsReturned as e:
        raise CommandError(f"{message_name} attribute {attribute_uri} returns multiple objects.") from e


def validate_attribute(attribute, message_name='', allow_descendants=None):
    if not isinstance(attribute, Attribute):
        raise CommandError(f"{message_name} attribute argument should be of type Attribute.")

    if not allow_descendants and attribute.get_descendants().exists():
        raise CommandError(f"{message_name} attribute '{attribute.uri}' with descendants is not supported.")


def get_valid_attribute(attribute, message_name='', allow_descendants=None):
    if isinstance(attribute, str):
        attribute = get_attribute_from_uri(attribute, message_name=message_name)

    validate_attribute(attribute, message_name=message_name, allow_descendants=allow_descendants)

    return attribute


def replace_attribute_on_related_model_instances(related_field, source=None, target=None, save_changes=False):
    model = related_field.related_model
    lookup_field = related_field.remote_field.name
    qs = model.objects.filter(**{lookup_field: source})

    replacement_results = []
    for instance in qs:
        instance_source = getattr(instance, lookup_field)

        if isinstance(instance_source, Attribute) and instance_source != source:
            raise CommandError("Instance attribute should be equal to the source attribute")

        setattr(instance, lookup_field, target)

        if save_changes:
            instance.save()
            logger.info(
                "Attribute %s on %s(id=%s) was replaced with %s.",
                source.uri, model._meta.verbose_name_raw, instance.id, target.uri
            )

        replacement_results.append({
            'model_name': model._meta.verbose_name_raw,
            'instance': instance,
            'source': source,
            'target': target,
            'saved': save_changes,
        })
    return replacement_results


def replace_attribute_in_view_template(source=None, target=None, save_changes=False, update_views=False):
    qs = View.objects.filter(**{"template__contains": source.path})
    replacement_results = []
    for instance in qs:

        template_target = replace_uri_in_template_string(instance.template, source.uri, target.uri)
        instance.template = template_target

        if save_changes and update_views:
            instance.save()
            logger.info(
                "Attribute %s in %s(id=%s) template was replaced with target %s.",
                source.uri, View._meta.verbose_name_raw, instance.id, target.uri
            )

        replacement_results.append({
            'model_name': View._meta.verbose_name_raw,
            'instance': instance,
            'source': source,
            'target': target,
            'saved': save_changes,
        })
    return replacement_results


def get_affected_projects_from_results(results):
    value_results = results.get(Value._meta.verbose_name_raw, [])
    return list({i['instance'].project for i in value_results})


def make_affected_elements_counts_message(results):
    element_counts = ", ".join([f"{k.capitalize()}({len(v)})" for k, v in results.items() if v])
    if not element_counts or not any(results.values()):
        return "No elements affected."
    affected_projects = get_affected_projects_from_results(results)
    if affected_projects:
        element_counts += f", Project({len(affected_projects)})"
    return f"Affected elements: {element_counts}"


def make_affected_projects_message(results):
    affected_projects = get_affected_projects_from_results(results)
    if not affected_projects:
        return "No Projects are affected."
    msg = "Affected Projects:"
    for project in affected_projects:
        msg += f"\n\t{project.id}\t{project}"
    return msg


def make_affected_views_message(results):
    view_results = results.get(View._meta.verbose_name_raw, [])
    if not view_results:
        return "No Views affected."
    msg = "Affected Views:"
    for view in {i['instance'] for i in view_results}:
        msg += f"\n\t{view.id}\t{view}"
    return msg


def make_affected_instances_detail_message(results):
    if not results:
        return ""
    msg = ""
    for k, merger_results in results.items():
        if not merger_results:
            continue
        msg += f"Merge attribute results for model {k.capitalize()} ({len(merger_results)})"
        msg += '\n'
        for result in merger_results:
            msg += dedent(f'''\

                {result['model_name']}(id={result['instance'].id})
                instance={result['instance']}
                source={result['source'].uri}
                target={result['target'].uri}
                saved={result['saved']}
            ''')
            if hasattr(result['instance'], 'project'):
                msg += f"Project(id={result['instance'].project.id}) {result['instance'].project}"
            msg += '\n'
        msg += '\n'
    return msg
