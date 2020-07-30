from rdmo.conditions.imports import import_condition
from rdmo.domain.imports import import_attribute
from rdmo.options.imports import import_option, import_optionset
from rdmo.questions.imports import (import_catalog, import_question,
                                    import_questionset, import_section)
from rdmo.tasks.imports import import_task
from rdmo.views.imports import import_view

PERMISSIONS = {
    'condition': (
        'conditions.add_condition', 'conditions.change_condition', 'conditions.delete_condition'
    ),
    'attribute': (
        'domain.add_attribute', 'domain.change_attribute', 'domain.delete_attribute'
    ),
    'optionset': (
        'options.add_optionset', 'options.change_optionset', 'options.delete_optionset'
    ),
    'option': (
        'options.add_option', 'options.change_option', 'options.delete_option'
    ),
    'catalog': (
        'questions.add_catalog', 'questions.change_catalog', 'questions.delete_catalog'
    ),
    'section': (
        'questions.add_section', 'questions.change_section', 'questions.delete_section'
    ),
    'questionset': (
        'questions.add_questionset', 'questions.change_questionset', 'questions.delete_questionset'
    ),
    'question': (
        'questions.add_question', 'questions.change_question', 'questions.delete_question'
    ),
    'task': (
        'tasks.add_task', 'tasks.change_task', 'tasks.delete_task'
    ),
    'view': (
        'views.add_view', 'views.change_view', 'views.delete_view'
    )
}


def check_permissions(elements, user):
    element_types = set([element.get('type') for element in elements])

    permissions = []
    for element_type in element_types:
        permissions += PERMISSIONS[element_type]

    return user.has_perms(permissions)


def import_elements(elements, save=[]):
    instances = []

    for element in elements:
        if element.get('type') == 'condition':
            instances.append(import_condition(element, save=save))

        elif element.get('type') == 'attribute':
            instances.append(import_attribute(element, save=save))

        elif element.get('type') == 'optionset':
            instances.append(import_optionset(element, save=save))

        elif element.get('type') == 'option':
            instances.append(import_option(element, save=save))

        elif element.get('type') == 'catalog':
            instances.append(import_catalog(element, save=save))

        elif element.get('type') == 'section':
            instances.append(import_section(element, save=save))

        elif element.get('type') == 'questionset':
            instances.append(import_questionset(element, save=save))

        elif element.get('type') == 'question':
            instances.append(import_question(element, save=save))

        elif element.get('type') == 'task':
            instances.append(import_task(element, save=save))

        elif element.get('type') == 'view':
            instances.append(import_view(element, save=save))

    return instances
