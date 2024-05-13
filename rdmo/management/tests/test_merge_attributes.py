import io
from string import Template
from typing import List, Union

import pytest

from django.core.management import CommandError, call_command

from rdmo.conditions.models import Condition
from rdmo.domain.models import Attribute
from rdmo.management.merge_attributes import ReplaceAttributeOnElements, model_helpers_with_attributes
from rdmo.options.models import Option
from rdmo.questions.models import Page, Question, QuestionSet, Section
from rdmo.views.models import View

ElementType = Union[Section, Page, QuestionSet, Question, Option, Condition]


EXAMPLE_URI_PREFIX = 'http://example.com/terms'
foo_merge_uri_prefix = 'http://foo-merge.com/terms'
bar_merge_uri_prefix = 'http://bar-merge.com/terms'
EXAMPLE_VIEW_URI_PATH = "views/view_a"
merge_view_template_addition_uri_path = 'individual/single/textarea'
merge_view_template_addition = Template("{% render_value '$new_uri' %}")
EXAMPLE_VIEW_URI = Attribute.build_uri(EXAMPLE_URI_PREFIX, merge_view_template_addition_uri_path)


new_merge_uri_prefixes = [foo_merge_uri_prefix, bar_merge_uri_prefix]

def _prepare_instance_for_copy(instance, uri_prefix=None, uri_path=None):
    instance.pk = None
    instance.id = None
    instance._state.adding = True
    if uri_prefix:
        instance.uri_prefix = uri_prefix
    if uri_path:
        instance.uri_path = uri_path
    return instance

def _add_new_line_to_view_template(model_helper, instance: View, new_uri_prefix: str) -> View:
    current_field_value = getattr(instance, model_helper.field_name)
    new_field_value = current_field_value + "\n"
    new_uri = Attribute.build_uri(new_uri_prefix, merge_view_template_addition_uri_path)
    new_field_value += merge_view_template_addition.substitute(new_uri=new_uri)
    setattr(instance, model_helper.field_name, new_field_value)
    return instance

def _create_copy_of_view_that_uses_new_attribute(model_helper, new_prefixes: List[str]):
    # TODO search in View.template for the attribute uri
    example_uri = f"{EXAMPLE_URI_PREFIX}/{EXAMPLE_VIEW_URI_PATH}"
    instance = model_helper.model.objects.get(uri=example_uri)
    for new_prefix in new_prefixes:
        instance = _prepare_instance_for_copy(instance, uri_prefix=new_prefix)
        instance.uri_path = EXAMPLE_VIEW_URI_PATH
        _add_new_line_to_view_template(model_helper, instance, new_prefix)
        instance.save()

def _create_copies_of_elements_with_new_uri_prefix(new_prefixes):
    for model_helper in model_helpers_with_attributes:
        if model_helper.field_introspection and model_helper.model == View:
            _create_copy_of_view_that_uses_new_attribute(model_helper, new_prefixes)
            continue   # skip this model_helper
        elif model_helper.field_introspection:
            continue  # skip this model_helper
        else:
            # create new model instances from example.com objects with the new uri_prefix
            filter_kwargs = {f"{model_helper.field_name}__uri_prefix": EXAMPLE_URI_PREFIX}
            example_objects = model_helper.model.objects.filter(**filter_kwargs)

        for new_prefix in new_prefixes:

            if not example_objects:
                continue
            for instance in example_objects:
                instance = _prepare_instance_for_copy(instance, uri_prefix=new_prefix)
                current_attribute = getattr(instance, model_helper.field_name)
                if not isinstance(current_attribute, Attribute):
                    continue
                filter_kwargs = {'path': current_attribute.path, 'uri_prefix': new_prefix}
                new_attribute = Attribute.objects.filter(**filter_kwargs).first()
                setattr(instance, model_helper.field_name, new_attribute)
                instance.save()

def _create_copies_of_attributes_with_new_uri_prefix(example_attributes, new_prefixes):
    for attribute in example_attributes:
        for new_prefix in new_prefixes:
            attribute = _prepare_instance_for_copy(attribute, uri_prefix=new_prefix)
            attribute.save()


@pytest.fixture
def create_merge_attributes(db, settings):
    """ Creates model instances for merge attributes tests """
    example_attributes = Attribute.objects.filter(uri_prefix=EXAMPLE_URI_PREFIX).all()
    _create_copies_of_attributes_with_new_uri_prefix(example_attributes, new_merge_uri_prefixes)
    _create_copies_of_elements_with_new_uri_prefix(new_merge_uri_prefixes)


@pytest.mark.parametrize('uri_prefix', new_merge_uri_prefixes)
def test_that_the_freshly_created_merge_attributes_are_present(create_merge_attributes, uri_prefix):
    merge_attributes = Attribute.objects.filter(uri_prefix=uri_prefix).all()
    assert len(merge_attributes) > 2
    unique_uri_prefixes = set(Attribute.objects.values_list("uri_prefix", flat=True))
    # test that the currently selected uri_prefix is in db
    assert uri_prefix in unique_uri_prefixes

    for attribute in merge_attributes:
        original_attribute = Attribute.objects.get(uri_prefix=EXAMPLE_URI_PREFIX, path=attribute.path)
        original_models_qs = [i.get_queryset(attribute=original_attribute) for i in model_helpers_with_attributes]
        if not any(len(i) > 0 for i in original_models_qs):
            continue  # skipt this attribute
        models_qs = [i.get_queryset(attribute=attribute) for i in model_helpers_with_attributes]
        assert any(len(i) > 0 for i in models_qs)

@pytest.mark.parametrize('source_uri_prefix', new_merge_uri_prefixes)
@pytest.mark.parametrize('save', [False, True])
def test_replacement_of_attributes_on_elements(create_merge_attributes, source_uri_prefix, save):
    source_attributes = Attribute.objects.filter(uri_prefix=source_uri_prefix).all()
    assert len(source_attributes) > 2
    unique_uri_prefixes = set(Attribute.objects.values_list("uri_prefix", flat=True))
    # test that the currently selected uri_prefix is in db
    assert source_uri_prefix in unique_uri_prefixes

    for source_attribute in source_attributes:
        target_attribute = Attribute.objects.get(uri_prefix=EXAMPLE_URI_PREFIX, path=source_attribute.path)
        failed, results = False, []
        if source_attribute.get_descendants() or target_attribute.get_descendants():
            with pytest.raises(ValueError):
                merger = ReplaceAttributeOnElements(source=source_attribute,
                                                    target=target_attribute,
                                                    model_helpers_with_attributes=model_helpers_with_attributes,
                                                    save=save)
            failed = True
        else:
            merger = ReplaceAttributeOnElements(source=source_attribute,
                                                target=target_attribute,
                                                model_helpers_with_attributes=model_helpers_with_attributes,
                                                save=save)
            results = [i for i in merger.results.values() if i]
        if not results:
            continue

        if save and not failed:
            # assert that the source attribut was deleted
            with pytest.raises(Attribute.DoesNotExist):
                Attribute.objects.get(id=source_attribute.id)

            if merge_view_template_addition_uri_path in source_attribute.path:
                # assert that the attribute in the view template was replaced as well
                view = View.objects.get(uri_prefix=source_uri_prefix, uri_path=EXAMPLE_VIEW_URI_PATH)
                assert any(EXAMPLE_VIEW_URI in i for i in view.template.splitlines())
                assert not any(source_attribute.uri in i for i in view.template.splitlines())
        else:
            assert Attribute.objects.get(id=source_attribute.id)


@pytest.mark.parametrize('source_uri_prefix', new_merge_uri_prefixes)
@pytest.mark.parametrize('save', [False, True])
def test_command_merge_attributes(create_merge_attributes, source_uri_prefix, save):
    source_attributes = Attribute.objects.filter(uri_prefix=source_uri_prefix).all()
    assert len(source_attributes) > 2
    unique_uri_prefixes = set(Attribute.objects.values_list("uri_prefix", flat=True))
    # test that the currently selected uri_prefix is in db
    assert source_uri_prefix in unique_uri_prefixes

    for source_attribute in source_attributes:
        target_attribute = Attribute.objects.get(uri_prefix=EXAMPLE_URI_PREFIX, path=source_attribute.path)
        stdout, stderr = io.StringIO(), io.StringIO()
        failed = False
        if source_attribute.get_descendants():
            with pytest.raises(CommandError):
                call_command('merge_attributes',
                     source=source_attribute.uri, target=target_attribute.uri, save=save,
                     stdout=stdout, stderr=stderr)
            failed = True
        elif target_attribute.get_descendants():
            with pytest.raises(CommandError):
                call_command('merge_attributes',
                             source=source_attribute.uri, target=target_attribute.uri, save=save,
                             stdout=stdout, stderr=stderr)
            failed = True
        else:
            call_command('merge_attributes',
                         source=source_attribute.uri, target=target_attribute.uri, save=save,
                         stdout=stdout, stderr=stderr)


        if save and not failed:
            # assert that the source attribut was deleted
            with pytest.raises(Attribute.DoesNotExist):
                Attribute.objects.get(id=source_attribute.id)

            if source_attribute.path in merge_view_template_addition_uri_path:
                # assert that the attribute in the view template was replaced as well
                view = View.objects.get(uri_prefix=source_uri_prefix, uri_path=EXAMPLE_VIEW_URI_PATH)
                assert any(EXAMPLE_VIEW_URI in i for i in view.template.splitlines())
                assert not any(source_attribute.uri in i for i in view.template.splitlines())
        else:
            assert Attribute.objects.get(id=source_attribute.id)
