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
    model_names = set([element.get('tag') for element in elements])

    permissions = []
    for model_name in model_names:
        permissions += PERMISSIONS[model_name]

    return user.has_perms(permissions)


def import_elements(elements, save=True):
    instances = []

    for element in elements:
        model_name = element.get('tag')

        if model_name == 'condition':
            instance = import_condition(element, save)

        elif model_name == 'attribute':
            instance = import_attribute(element, save)

        elif model_name == 'optionset':
            instance = import_optionset(element, save)

        elif model_name == 'option':
            instance = import_option(element, save)

        elif model_name == 'catalog':
            instance = import_catalog(element, save)

        elif model_name == 'section':
            instance = import_section(element, save)

        elif model_name == 'page':
            instance = import_page(element, save)

        elif model_name == 'questionset':
            instance = import_questionset(element, save)

        elif model_name == 'question':
            instance = import_question(element, save)

        elif model_name == 'task':
            instance = import_task(element, save)

        elif model_name == 'view':
            instance = import_view(element, save)

        else:
            instance = None

        instances.append(instance)

    return instances
