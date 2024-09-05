from dataclasses import dataclass
from typing import List

from rdmo.conditions.models import Condition
from rdmo.core.models import Model
from rdmo.domain.models import Attribute
from rdmo.options.models import Option, OptionSet
from rdmo.questions.models import Catalog, Question, Section
from rdmo.questions.models import Page as PageModel
from rdmo.questions.models.questionset import QuestionSet
from rdmo.tasks.models import Task
from rdmo.views.models import View


@dataclass
class ModelHelper:
    """Helper class to bundle information about models for test cases."""

    model: Model
    form_field: str = "URI Path"
    db_field: str = "uri_path"
    has_nested: bool = False

    @property
    def url(self) -> str:
        return f"{self.model._meta.model_name}s"

    @property
    def verbose_name(self) -> str:
        """Return the verbose_name for the model."""
        return self.model._meta.verbose_name

    @property
    def verbose_name_plural(self) -> str:
        """Return the verbose_name_plural for the model."""
        return self.model._meta.verbose_name_plural



model_helpers = (
    ModelHelper(Catalog, has_nested=True),
    ModelHelper(Section, has_nested=True),
    ModelHelper(PageModel, has_nested=True),
    ModelHelper(QuestionSet, has_nested=True),
    ModelHelper(Question),
    ModelHelper(
        Attribute, has_nested=True, form_field="Key", db_field="key"
    ),
    ModelHelper(OptionSet, has_nested=True),
    ModelHelper(Option),
    ModelHelper(Condition),
    ModelHelper(Task),
    ModelHelper(View),
)


def delete_all_objects(db_models: List):
    for db_model in db_models:
        db_model.objects.all().delete()
