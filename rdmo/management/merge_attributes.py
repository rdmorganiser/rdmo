from dataclasses import dataclass, field
from textwrap import dedent
from typing import Callable, Dict, List, Optional, Tuple, Type, Union

from django.db import models
from django.db.models import QuerySet

from rdmo.conditions.models import Condition
from rdmo.domain.models import Attribute
from rdmo.management.utils import replace_uri_in_template_string
from rdmo.projects.models import Value
from rdmo.questions.models import Page, Question, QuestionSet
from rdmo.tasks.models import Task
from rdmo.views.models import View


@dataclass
class ModelsWithAttributeHelper:
    model: Type[models.Model]
    field_name: str = field(default='attribute')
    field_introspection: bool = field(default=False)
    replacement_function: Callable = field(default=None)

    def __post_init__(self):
        _field_model = self.model._meta.get_field(self.field_name).related_model
        if not isinstance(_field_model, type(Attribute)) and not self.field_introspection:
            raise ValueError(f"field {self.field_name} on the model {self.model_name} is not an attribute")
        elif self.field_introspection and self.replacement_function is None:
            raise ValueError(f"field {self.field_name} on the model {self.model_name} requires a replacement function")

    def get_queryset(self, attribute: Optional[Attribute]=None) -> QuerySet:
        if attribute is None:
            raise ValueError("attribute is required")
        if self.field_introspection:
            return self.model.objects.filter(**{f"{self.field_name}__contains": attribute.path})
        return self.model.objects.filter(**{self.field_name: attribute})

    @property
    def model_name(self):
        return self.model._meta.model_name.capitalize()

    def replace_attribute_on_instance(self,
                                      instance: models.Model,
                                      source: Attribute,
                                      target: Attribute) -> models.Model:
        instance_field = getattr(instance, self.field_name)

        if isinstance(instance_field, Attribute) and not instance_field == source:  # just to double-check
            raise ValueError("Instance attribute should be equal to the source attribute")
        elif not isinstance(instance_field, Attribute) and not self.field_introspection:
            raise ValueError("When instance field is not an attribute, it should use field introspection")

        replacement_field = target
        if self.field_introspection:  # for when the attribute is "hidden as string" within the field
            replacement_field = self.replacement_function(instance_field, source, target)

        setattr(instance, self.field_name, replacement_field)

        return instance

model_helpers_with_attributes = (
    ModelsWithAttributeHelper(Page), ModelsWithAttributeHelper(QuestionSet), ModelsWithAttributeHelper(Question),
    ModelsWithAttributeHelper(Condition, field_name='source'),
    ModelsWithAttributeHelper(Task, field_name='start_attribute'),
    ModelsWithAttributeHelper(Task, field_name='end_attribute'),
    ModelsWithAttributeHelper(Value),
    ModelsWithAttributeHelper(View, field_name='template',
                              field_introspection=True,
                              replacement_function=replace_uri_in_template_string),
)


@dataclass
class AttributeReplacementModelResult:
    model_helper: Optional[ModelsWithAttributeHelper] = field(default=None)
    source: Optional[Attribute] = field(default=None)
    target: Optional[Attribute] = field(default=None)
    instance:  Optional[models.Model] = field(default=None)
    saved: bool = field(default=False)

    def __repr__(self):
        _repr = (f"""\
            Model={self.model_helper.model_name}
            instance={self.instance}
            source={self.source.uri}
            source_exists={self.source_exists}
            target={self.target.uri}
            saved={self.saved}""")
        _repr = dedent(_repr)
        if hasattr(self.instance, 'project'):
            _repr += f"\nproject={self.instance.project}"
        _repr += "\n"
        return _repr

    @property
    def source_exists(self) -> bool:
        if self.source.id is None:
            return False
        return self.model_helper.get_queryset(self.source).exists()

def replace_attribute_on_element_instances(
        model_helper: ModelsWithAttributeHelper,
        source_attribute: Attribute,
        target_attribute: Attribute,
        save: bool
) -> List[AttributeReplacementModelResult]:
    qs = model_helper.get_queryset(attribute=source_attribute)
    replaced_attributes = []
    for instance in qs:
        instance = model_helper.replace_attribute_on_instance(instance, source_attribute, target_attribute)
        if save:
            instance.save()  # need to use save to trigger save method on model instances
        replaced_attributes.append(
            AttributeReplacementModelResult(
                model_helper=model_helper,
                source=source_attribute,
                target=target_attribute,
                instance=instance,
                saved=save
            )
        )
    return replaced_attributes


AttributeReplacementResultDict = Dict[str, List[AttributeReplacementModelResult]]


def results_message(results: AttributeReplacementResultDict) -> str:
    if not results:
        return ""
    # counts = {k: len(v) for k, v in results.items() if v}
    # {k: set(i.source for i in v) for k, v in results.items() if v}
    _msg = ""
    for k, merger_results in results.items():
        if not merger_results:
            continue
        _msg += f"Merger results for model {k.capitalize()} ({len(merger_results)})"
        for result in merger_results:
            _msg += f"\t{result}"

    element_counts = ", ".join([f"{k.capitalize()}({len(v)})" for k, v in results.items() if v])
    _msg += f"\nAffected elements: {element_counts}"
    if 'Value' in results.keys():
        _msg += "\nAffected Projects:"
        for project in {i.instance.project for i in results['Value']}:
            _msg += f"\n\tproject={project} (id={project.id})"
    return _msg


@dataclass
class ReplaceAttributeOnElements:

    source: Optional[Attribute] = field(default=None)
    target: Optional[Attribute] = field(default=None)
    model_helpers_with_attributes: Tuple[ModelsWithAttributeHelper] = model_helpers_with_attributes
    save: bool = field(default=False)
    results: AttributeReplacementResultDict = field(default_factory=dict)
    verbosity: int = field(default=0)

    def __post_init__(self):

        self.source = get_valid_attribute(self.source, message_name='Source')
        self.target = get_valid_attribute(self.target, message_name='Target')

        if self.source == self.target:
            raise ValueError("Source and Target attribute are the same.")

        self.results = self.run_attribute_replacement_over_models(save=self.save)
        if self.save and all(a.saved for i in self.results.values() for a in i):
            try:
                self.source.delete()
            except self.source.DoesNotExist:
                pass
        if self.verbosity >= 1:
            print(results_message(self.results))
            if self.save:
                print(self.save_message())

    def save_message(self) -> str:
        _msg = f"Source attribute {self.source.uri} was replaced with {self.target.uri}."
        _msg += f"\nSource attribute {self.source.uri} was deleted."
        return _msg


    def run_attribute_replacement_over_models(self, save=False) -> AttributeReplacementResultDict:
        """ replaces the source attribute with target attribute on all elements of model_helpers_with_attributes """
        results = {}
        for model_helper in self.model_helpers_with_attributes:
            replaced_attributes = replace_attribute_on_element_instances(model_helper,
                                                                          self.source,
                                                                          self.target,
                                                                          save)
            results[model_helper.model_name] = replaced_attributes
        return results


def get_valid_attribute(attribute: Union[str, Attribute], message_name: str = '') -> Attribute:
    """ get an valid attribute instance from string (uri) or instance"""
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

    if attribute.get_descendants():
        raise ValueError(f"{message_name} attributes '{attribute}' with descendants are not (yet) supported.")

    return attribute
