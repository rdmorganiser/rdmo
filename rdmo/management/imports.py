from rdmo.conditions.imports import import_condition
from rdmo.core.constants import PERMISSIONS
from rdmo.domain.imports import import_attribute
from rdmo.options.imports import (import_option,
                                  import_optionset)
from rdmo.questions.imports import (import_catalog,
                                    import_question, import_questionset,
                                    import_section, import_page)
from rdmo.tasks.imports import import_task
from rdmo.views.imports import import_view


def check_permissions(elements, user):
    element_types = set([element.get('type') for element in elements])

    permissions = []
    for element_type in element_types:
        permissions += PERMISSIONS[element_type]

    return user.has_perms(permissions)


def import_elements(elements, save=True):
    instances = []

    for element in elements:
        element_type = element.get('type')

        if element_type == 'condition':
            instance = import_condition(element, save)

        elif element_type == 'attribute':
            instance = import_attribute(element, save)

        elif element_type == 'optionset':
            instance = import_optionset(element, save)

        elif element_type == 'option':
            instance = import_option(element, save)

        elif element_type == 'catalog':
            instance = import_catalog(element, save)

        elif element_type == 'section':
            instance = import_section(element, save)

        elif element_type == 'page':
            instance = import_page(element, save)

        elif element_type == 'questionset':
            instance = import_questionset(element, save)

        elif element_type == 'question':
            instance = import_question(element, save)

        elif element_type == 'task':
            instance = import_task(element, save)

        elif element_type == 'view':
            instance = import_view(element, save)

        else:
            instance = None

        instances.append(instance)

    return instances
