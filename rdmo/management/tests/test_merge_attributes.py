import io
from string import Template
from typing import List, Union

import pytest

from django.core.management import CommandError, call_command

from rdmo.conditions.models import Condition
from rdmo.domain.models import Attribute
from rdmo.options.models import Option
from rdmo.questions.models import Page, Question, QuestionSet, Section
from rdmo.views.models import View

ElementType = Union[Section, Page, QuestionSet, Question, Option, Condition]

ATTRIBUTE_RELATED_MODELS_FIELDS = [i for i in Attribute._meta.get_fields()
                                   if i.is_relation and not i.many_to_many
                                   and i.related_model is not Attribute]

EXAMPLE_URI_PREFIX = 'http://example.com/terms'
FOO_MERGE_URI_PREFIX = 'http://foo-merge.com/terms'
BAR_MERGE_URI_PREFIX = 'http://bar-merge.com/terms'
EXAMPLE_VIEW_URI_PATH = "views/view_a"
VIEW_TEMPLATE_URI_PATH = 'individual/single/textarea'
VIEW_TEMPLATE_URI_PATH_ADDITIONS = ['', '/test1', '/test2', '/testfoo']
VIEW_TEMPLATE_RENDER_VALUE = Template("{% render_value '$new_uri' %}")
EXAMPLE_VIEW_URI = Attribute.build_uri(EXAMPLE_URI_PREFIX, VIEW_TEMPLATE_URI_PATH)
NEW_MERGE_URI_PREFIXES = [FOO_MERGE_URI_PREFIX, BAR_MERGE_URI_PREFIX]


def _prepare_instance_for_copy(instance, uri_prefix=None, uri_path=None):
    instance.pk = None
    instance.id = None
    instance._state.adding = True
    if uri_prefix:
        instance.uri_prefix = uri_prefix
    if uri_path:
        instance.uri_path = uri_path
    return instance


def _get_queryset(related_field, attribute=None):
    model = related_field.related_model
    if model is View:
        return model.objects.filter(**{"template__contains": attribute.path})
    lookup_field = related_field.remote_field.name
    return model.objects.filter(**{lookup_field: attribute})


def create_new_uris_with_uri_prefix_for_template(new_uri_prefix: str) -> List[str]:
    new_uris = []
    for extra_path in VIEW_TEMPLATE_URI_PATH_ADDITIONS:
        new_uri_path = VIEW_TEMPLATE_URI_PATH + extra_path
        new_uri = Attribute.build_uri(new_uri_prefix, new_uri_path)
        new_uris.append(new_uri)
    return new_uris


def create_copy_of_view_that_uses_new_attribute(db, new_prefixes: List[str]):
    qs = View.objects.filter(**{"uri__contains": EXAMPLE_VIEW_URI_PATH}).all()
    if not qs.exists():
        raise ValueError("Views for tests should exist here.")
    for instance in qs:
        original_template = instance.template
        for new_prefix in new_prefixes:
            instance = _prepare_instance_for_copy(instance, uri_prefix=new_prefix, uri_path=EXAMPLE_VIEW_URI_PATH)
            new_template_uris = create_new_uris_with_uri_prefix_for_template(new_prefix)
            new_template = ''
            new_template += original_template
            for uri in new_template_uris:
                new_template += '\n'
                new_template += VIEW_TEMPLATE_RENDER_VALUE.substitute(new_uri=uri)
            instance.template = new_template
            instance.save()


def create_copies_of_related_models_with_new_uri_prefix(new_prefixes):
    for related_model_field in ATTRIBUTE_RELATED_MODELS_FIELDS:
        model = related_model_field.related_model
        lookup_field = related_model_field.remote_field.name
        # create new model instances from example.com objects with the new uri_prefix
        filter_kwargs = {f"{lookup_field}__uri_prefix": EXAMPLE_URI_PREFIX}
        example_objects = model.objects.filter(**filter_kwargs)

        for new_prefix in new_prefixes:

            if not example_objects:
                continue
            for instance in example_objects:
                instance = _prepare_instance_for_copy(instance, uri_prefix=new_prefix)
                current_attribute = getattr(instance, lookup_field)
                if not isinstance(current_attribute, Attribute):
                    continue
                filter_kwargs = {'path': current_attribute.path, 'uri_prefix': new_prefix}
                new_attribute = Attribute.objects.filter(**filter_kwargs).first()
                setattr(instance, lookup_field, new_attribute)
                instance.save()


def create_copies_of_attributes_with_new_uri_prefix(example_attributes, new_prefixes):
    for attribute in example_attributes:
        for new_prefix in new_prefixes:
            attribute = _prepare_instance_for_copy(attribute, uri_prefix=new_prefix)
            attribute.save()


def get_related_affected_instances(attribute) -> list:
    related_qs = []
    for related_field in ATTRIBUTE_RELATED_MODELS_FIELDS:
        model = related_field.related_model
        lookup_field = related_field.remote_field.name
        qs = model.objects.filter(**{lookup_field: attribute})
        related_qs.append(qs)
    return related_qs


@pytest.fixture
def _create_new_merge_attributes_and_views(db, settings):
    """ Creates model instances for merge attributes tests """
    example_attributes = Attribute.objects.filter(uri_prefix=EXAMPLE_URI_PREFIX).all()
    create_copies_of_attributes_with_new_uri_prefix(example_attributes, NEW_MERGE_URI_PREFIXES)
    create_copies_of_related_models_with_new_uri_prefix(NEW_MERGE_URI_PREFIXES)
    create_copy_of_view_that_uses_new_attribute(db, NEW_MERGE_URI_PREFIXES)


@pytest.mark.usefixtures("_create_new_merge_attributes_and_views")
def test_command_merge_attributes_fails_correctly(db, settings):
    first_parent_attribute = Attribute.objects.exclude(parent=None).first().parent
    first_leaf_attribute = None
    for attribute in Attribute.objects.all():
        if not attribute.get_descendants().exists():
            first_leaf_attribute = attribute
            break

    source_and_target_are_the_same = {
        'source': first_parent_attribute,
        'target': first_parent_attribute
    }
    stdout, stderr = io.StringIO(), io.StringIO()
    with pytest.raises(CommandError):
        call_command('merge_attributes',
                     stdout=stdout, stderr=stderr, **source_and_target_are_the_same)

    source_has_descendants = {
        'source': first_parent_attribute,
        'target': first_leaf_attribute
    }
    stdout, stderr = io.StringIO(), io.StringIO()
    with pytest.raises(CommandError):
        call_command('merge_attributes',
                     stdout=stdout, stderr=stderr, **source_has_descendants)

    source_does_not_exist = {
        'source': 'http://uri-does-not-exist-1.com',
        'target': first_leaf_attribute
    }
    stdout, stderr = io.StringIO(), io.StringIO()
    with pytest.raises(CommandError):
        call_command('merge_attributes',
                     stdout=stdout, stderr=stderr, **source_does_not_exist)

    target_does_not_exist = {
        'source': first_leaf_attribute,
        'target': 'http://uri-does-not-exist-1.com',
    }
    stdout, stderr = io.StringIO(), io.StringIO()
    with pytest.raises(CommandError):
        call_command('merge_attributes',
                     stdout=stdout, stderr=stderr, **target_does_not_exist)


@pytest.mark.parametrize('uri_prefix', NEW_MERGE_URI_PREFIXES)
@pytest.mark.usefixtures("_create_new_merge_attributes_and_views")
def test_that_the_freshly_created_merge_attributes_are_present(db, uri_prefix):
    merge_attributes_uris = Attribute.objects.filter(
        uri_prefix=uri_prefix).all().values_list(
        'uri', flat=True).distinct()
    assert len(merge_attributes_uris) > 2
    unique_uri_prefixes = set(Attribute.objects.values_list("uri_prefix", flat=True))
    # test that the currently selected uri_prefix is in db
    assert uri_prefix in unique_uri_prefixes

    for attribute_uri in merge_attributes_uris:
        attribute = Attribute.objects.get(uri=attribute_uri)
        original_attribute = Attribute.objects.get(uri_prefix=EXAMPLE_URI_PREFIX, path=attribute.path)
        original_models_qs = [_get_queryset(i, attribute=original_attribute) for i in ATTRIBUTE_RELATED_MODELS_FIELDS]
        if not any(len(i) > 0 for i in original_models_qs):
            continue  # skip this attribute
        models_qs = [_get_queryset(i, attribute=attribute) for i in ATTRIBUTE_RELATED_MODELS_FIELDS]
        assert any(len(i) > 0 for i in models_qs)

    # assert new views created by create_copy_of_view_that_uses_new_attribute
    # foo-merge
    foo_merge_view_qs = View.objects.filter(template__contains=FOO_MERGE_URI_PREFIX).exclude(
        template__contains=BAR_MERGE_URI_PREFIX)
    assert foo_merge_view_qs.count() == 1
    assert foo_merge_view_qs.first().uri_prefix == FOO_MERGE_URI_PREFIX
    # bar-merge
    bar_merge_view_qs = View.objects.filter(template__contains=BAR_MERGE_URI_PREFIX).exclude(
        template__contains=FOO_MERGE_URI_PREFIX)
    assert bar_merge_view_qs.count() == 1
    assert bar_merge_view_qs.first().uri_prefix == BAR_MERGE_URI_PREFIX


@pytest.mark.parametrize('source_uri_prefix', NEW_MERGE_URI_PREFIXES)
@pytest.mark.parametrize('save', [False, True])
@pytest.mark.parametrize('delete', [False, True])
@pytest.mark.parametrize('view', [False, True])
@pytest.mark.usefixtures("_create_new_merge_attributes_and_views")
def test_command_merge_attributes(db, settings, source_uri_prefix, save, delete, view):
    source_attribute_uris = Attribute.objects.filter(
        uri_prefix=source_uri_prefix).all().values_list(
        'uri', flat=True).distinct()
    assert len(source_attribute_uris) > 2
    unique_uri_prefixes = set(Attribute.objects.values_list("uri_prefix", flat=True))
    # test that the currently selected uri_prefix is in db
    assert source_uri_prefix in unique_uri_prefixes

    for source_attribute_uri in source_attribute_uris:
        source_attribute = Attribute.objects.get(uri=source_attribute_uri)
        target_attribute = Attribute.objects.get(uri_prefix=EXAMPLE_URI_PREFIX, path=source_attribute.path)
        before_source_related_qs = get_related_affected_instances(source_attribute)
        # before_target_related_qs = get_related_affected_instances(target_attribute)

        command_kwargs = {'source': source_attribute.uri,
                          'target': target_attribute.uri,
                          'save': save, 'delete': delete, 'view': view}
        failed = False

        if source_attribute.get_descendants():
            stdout, stderr = io.StringIO(), io.StringIO()
            with pytest.raises(CommandError):
                call_command('merge_attributes',
                             stdout=stdout, stderr=stderr, **command_kwargs)
            failed = True
        else:
            stdout, stderr = io.StringIO(), io.StringIO()
            call_command('merge_attributes',
                         stdout=stdout, stderr=stderr, **command_kwargs)

        if delete and not failed:
            # assert that the source attribute was deleted
            with pytest.raises(Attribute.DoesNotExist):
                Attribute.objects.get(id=source_attribute.id)
        else:
            assert Attribute.objects.get(id=source_attribute.id)

        after_source_related_qs = get_related_affected_instances(source_attribute)
        after_target_related_qs = get_related_affected_instances(target_attribute)

        if save and not failed:

            if any(i.exists() for i in before_source_related_qs):
                assert not any(i.exists() for i in after_source_related_qs)
                assert any(i.exists() for i in after_target_related_qs)
        else:
            if any(i.exists() for i in before_source_related_qs):
                assert any(i.exists() for i in after_source_related_qs)


@pytest.mark.parametrize('source_uri_prefix', NEW_MERGE_URI_PREFIXES)
@pytest.mark.parametrize('save', [False, True])
@pytest.mark.parametrize('delete', [False, True])
@pytest.mark.parametrize('view', [False, True])
@pytest.mark.usefixtures("_create_new_merge_attributes_and_views")
def test_command_merge_attributes_for_views(db, settings, source_uri_prefix, save, delete, view):
    source_attributes = Attribute.objects.filter(uri_prefix=source_uri_prefix).all()
    assert len(source_attributes) > 2
    unique_uri_prefixes = set(Attribute.objects.values_list("uri_prefix", flat=True))
    # test that the currently selected uri_prefix is in db
    assert source_uri_prefix in unique_uri_prefixes
    source_attribute_uri = Attribute.build_uri(uri_prefix=source_uri_prefix, path=VIEW_TEMPLATE_URI_PATH)
    target_attribute_uri = Attribute.build_uri(uri_prefix=EXAMPLE_URI_PREFIX, path=VIEW_TEMPLATE_URI_PATH)

    stdout, stderr = io.StringIO(), io.StringIO()
    before_source_related_view_uri_qs = View.objects.filter(**{"template__contains": f"'{source_attribute_uri}'"}).all()

    before_source_related_view_uri_templates = {i.uri: i.template for i in before_source_related_view_uri_qs}

    command_kwargs = {'source': source_attribute_uri,
                      'target': target_attribute_uri,
                      'save': save, 'delete': delete, 'view': view}
    failed = False
    call_command('merge_attributes',
                 stdout=stdout, stderr=stderr, **command_kwargs)

    if delete and not failed:
        # assert that the source attribute was deleted
        with pytest.raises(Attribute.DoesNotExist):
            Attribute.objects.get(uri=source_attribute_uri)
    else:
        assert Attribute.objects.get(uri=source_attribute_uri)

    after_source_related_view_uri_qs = View.objects.filter(**{"template__contains": f"'{source_attribute_uri}'"})
    after_target_related_view_uri_qs = View.objects.filter(**{"template__contains": f"'{target_attribute_uri}'"})

    if not save or not view:
        assert not after_target_related_view_uri_qs.exists()
        return

    if save and not failed:
        pass

    if (save and not failed and view
            and VIEW_TEMPLATE_URI_PATH in source_attribute_uri):
        # assert that the attribute in the view template was replaced as well
        # the EXAMPLE_VIEW_URI is from the target attribute
        # uri_prefix = source_uri_prefix, uri_path = EXAMPLE_VIEW_URI_PATH
        assert not after_source_related_view_uri_qs.exists()
        assert after_target_related_view_uri_qs.exists()

        if (before_source_related_view_uri_templates and
                source_attribute_uri != target_attribute_uri):
            after_occurrences = list(filter(lambda x: target_attribute_uri in x,
                                            after_target_related_view_uri_qs.first().template.splitlines()))
            assert len(after_occurrences) == 1
            before_occurrences = list(filter(lambda x: target_attribute_uri in x,
                                             before_source_related_view_uri_qs.first().template.splitlines()))
            assert len(before_occurrences) == 0
