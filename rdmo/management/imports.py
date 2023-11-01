from collections import defaultdict

from rdmo.conditions.imports import import_condition
from rdmo.domain.imports import import_attribute
from rdmo.options.imports import import_option, import_optionset
from rdmo.questions.imports import import_catalog, import_page, import_question, import_questionset, import_section
from rdmo.tasks.imports import import_task
from rdmo.views.imports import import_view

ELEMENT_IMPORT_METHODS = {
    "conditions.condition": import_condition,
    "domain.attribute": import_attribute,
    "options.optionset": import_optionset,
    "options.option": import_option,
    "questions.catalog": import_catalog,
    "questions.section": import_section,
    "questions.page": import_page,
    "questions.questionset": import_questionset,
    "questions.question": import_question,
    "tasks.task": import_task,
    "views.view": import_view,
}


def import_elements(elements, save=True, user=None):
    for element in elements:
        model = element.get('model')

        element.update({
            'warnings': defaultdict(list),
            'errors': [],
            'created': False,
            'updated': False
        })

        import_method = ELEMENT_IMPORT_METHODS[model]
        import_method(element, save, user)

        element = filter_warnings(element, elements)


def filter_warnings(element, elements):
    # remove warnings regarding elements which are in the elements list
    warnings = []
    for uri, messages in element['warnings'].items():
        if not next(filter(lambda e: e['uri'] == uri, elements), None):
            warnings += messages

    element['warnings'] = warnings
    return element
