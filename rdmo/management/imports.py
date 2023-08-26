from collections import defaultdict

from rdmo.conditions.imports import import_condition
from rdmo.domain.imports import import_attribute
from rdmo.options.imports import import_option, import_optionset
from rdmo.questions.imports import import_catalog, import_page, import_question, import_questionset, import_section
from rdmo.tasks.imports import import_task
from rdmo.views.imports import import_view


def import_elements(elements, save=True, user=None):
    for element in elements:
        model = element.get('model')

        element.update({
            'warnings': defaultdict(list),
            'errors': [],
            'created': False,
            'updated': False
        })

        if model == 'conditions.condition':
            import_condition(element, save, user)

        elif model == 'domain.attribute':
            import_attribute(element, save, user)

        elif model == 'options.optionset':
            import_optionset(element, save, user)

        elif model == 'options.option':
            import_option(element, save, user)

        elif model == 'questions.catalog':
            import_catalog(element, save, user)

        elif model == 'questions.section':
            import_section(element, save, user)

        elif model == 'questions.page':
            import_page(element, save, user)

        elif model == 'questions.questionset':
            import_questionset(element, save, user)

        elif model == 'questions.question':
            import_question(element, save, user)

        elif model == 'tasks.task':
            import_task(element, save, user)

        elif model == 'views.view':
            import_view(element, save, user)

        element = filter_warnings(element, elements)


def filter_warnings(element, elements):
    # remove warnings regarding elements which are in the elements list
    warnings = []
    for uri, messages in element['warnings'].items():
        if not next(filter(lambda e: e['uri'] == uri, elements), None):
            warnings += messages

    element['warnings'] = warnings
    return element
