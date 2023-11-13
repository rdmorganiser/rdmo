import logging
from collections import defaultdict
from typing import Optional

from django.db import models
from django.forms.models import model_to_dict

from rdmo.conditions.imports import import_condition
from rdmo.conditions.validators import ConditionLockedValidator, ConditionUniqueURIValidator
from rdmo.core.imports import common_import_methods
from rdmo.domain.imports import import_attribute
from rdmo.domain.validators import AttributeLockedValidator, AttributeParentValidator, AttributeUniqueURIValidator
from rdmo.options.imports import import_option, import_optionset
from rdmo.options.validators import (
    OptionLockedValidator,
    OptionSetLockedValidator,
    OptionSetUniqueURIValidator,
    OptionUniqueURIValidator,
)
from rdmo.questions.imports import import_catalog, import_page, import_question, import_questionset, import_section
from rdmo.questions.validators import (
    CatalogLockedValidator,
    CatalogUniqueURIValidator,
    PageLockedValidator,
    PageUniqueURIValidator,
    QuestionLockedValidator,
    QuestionSetLockedValidator,
    QuestionSetUniqueURIValidator,
    QuestionUniqueURIValidator,
    SectionLockedValidator,
    SectionUniqueURIValidator,
)
from rdmo.tasks.imports import import_task
from rdmo.tasks.validators import TaskLockedValidator, TaskUniqueURIValidator
from rdmo.views.imports import import_view
from rdmo.views.validators import ViewLockedValidator, ViewUniqueURIValidator

logger = logging.getLogger(__name__)

ELEMENT_MODEL_IMPORT_MAPPER = {
    "conditions.condition": {
        "dotted_path": 'rdmo.conditions.models.Condition',
        "import_method": import_condition,
        "validators": (ConditionLockedValidator, ConditionUniqueURIValidator)
    },
    "domain.attribute": {
        "dotted_path": 'rdmo.domain.models.Attribute',
        "import_method": import_attribute,
        "validators": (AttributeLockedValidator, AttributeParentValidator, AttributeUniqueURIValidator)
    },
    "options.optionset": {
        "dotted_path": "rdmo.options.models.OptionSet",
        "import_method": import_optionset,
        "validators": (OptionSetLockedValidator, OptionSetUniqueURIValidator),
    },
    "options.option": {
        "dotted_path": "rdmo.options.models.Option",
        "import_method": import_option,
        "validators": (OptionLockedValidator, OptionUniqueURIValidator),
    },
    "questions.catalog": {
        "dotted_path": "rdmo.questions.models.catalog.Catalog",
        "import_method": import_catalog,
        "validators": (CatalogLockedValidator, CatalogUniqueURIValidator),
    },
    "questions.section": {
        "dotted_path": "rdmo.questions.models.section.Section",
        "import_method": import_section,
        "validators": (SectionLockedValidator, SectionUniqueURIValidator),
    },
    "questions.page": {
        "dotted_path": "rdmo.questions.models.page.Page",
        "import_method": import_page,
        "validators":  (PageLockedValidator, PageUniqueURIValidator),
    },
    "questions.questionset": {
        "dotted_path": "rdmo.questions.models.questionset.QuestionSet",
        "import_method": import_questionset,
        "validators": (QuestionSetLockedValidator, QuestionSetUniqueURIValidator),
    },
    "questions.question": {
        "dotted_path": "rdmo.questions.models.question.Question",
        "import_method": import_question,
        "validators": (QuestionLockedValidator, QuestionUniqueURIValidator),
    },
    "tasks.task": {
        "dotted_path": "rdmo.tasks.models.Task",
        "import_method": import_task,
        "validators": (TaskLockedValidator, TaskUniqueURIValidator),
    },
    "views.view": {
        "dotted_path": "rdmo.views.models.View",
        "import_method": import_view,
        "validators": (ViewLockedValidator, ViewUniqueURIValidator),
    },
}


def import_elements(uploaded_elements, save=True, user=None):
    imported_elements = []
    for element in uploaded_elements:
        model = element.get('model')
        if model is None:
            continue
        element = import_element(model_path=model, element=element, save=save, user=user)
        element = filter_warnings(element, uploaded_elements)
        imported_elements.append(element)
    return imported_elements


def filter_warnings(element, elements):
    # remove warnings regarding elements which are in the elements list
    warnings = []
    for uri, messages in element['warnings'].items():
        if not next(filter(lambda e: e['uri'] == uri, elements), None):
            warnings += messages

    element['warnings'] = warnings
    return element


def import_element(
        model_path: Optional[str] = None,
        element: Optional[dict] = None,
        save: bool = True,
        user = None
    ):

    if element is None:
        return element

    element.update({
        'warnings': defaultdict(list),
        'errors': [],
        'created': False,
        'updated': False,
        'original': defaultdict()
    })

    if model_path is None:
        return element

    model_import = ELEMENT_MODEL_IMPORT_MAPPER[model_path]
    import_method = model_import['import_method']
    model_path = model_import['dotted_path']
    validators = model_import['validators']

    instance, element, _msg, _created = common_import_methods(
                            model_path,
                            uri=element.get('uri'),
                            element=element
                    )
    _updated = not _created
    # for when the element is updated
    # keep a dict of the original
    # needs to be created here, else the changes will be overwritten
    original = model_to_dict(instance) if _updated else {}

    instance = import_method(instance, element, validators, save, user)

    if element.get('errors'):
        return element

    if save:
        logger.info(_msg)
        element['created'] = _created
        element['updated'] = _updated

    if _updated:
        original = filter_original(element, original)
        element['updated'] = _updated
        element['original'] = original

    return element


def filter_original(element, original):
    '''select only keys for original that are in the element.'''
    # filter for keys
    original = {
        k: val for k, val in
        original.items()
        if k in element
    }
    # replace the lists of nested model values
    # in the "original" dict
    original_replace = {
        k: element[k] for k, val in
        original.items() if (
            isinstance(val, list) and
            any(isinstance(i, models.Model) for i in val)
        )
    }
    original.update(**original_replace)
    return original
