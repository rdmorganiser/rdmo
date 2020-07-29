from rdmo.conditions.imports import import_condition
from rdmo.core.xml import flat_xml_to_elements
from rdmo.domain.imports import import_attribute
from rdmo.options.imports import import_option, import_optionset
from rdmo.questions.imports import (import_catalog, import_question,
                                    import_questionset, import_section)
from rdmo.tasks.imports import import_task
from rdmo.views.imports import import_view


def import_elements(root, save=[]):
    elements = []

    for element in flat_xml_to_elements(root):
        if element.get('type') == 'condition':
            elements.append(import_condition(element, save=save))

        elif element.get('type') == 'attribute':
            elements.append(import_attribute(element, save=save))

        elif element.get('type') == 'optionset':
            elements.append(import_optionset(element, save=save))

        elif element.get('type') == 'option':
            elements.append(import_option(element, save=save))

        elif element.get('type') == 'catalog':
            elements.append(import_catalog(element, save=save))

        elif element.get('type') == 'section':
            elements.append(import_section(element, save=save))

        elif element.get('type') == 'questionset':
            elements.append(import_questionset(element, save=save))

        elif element.get('type') == 'question':
            elements.append(import_question(element, save=save))

        elif element.get('type') == 'task':
            elements.append(import_task(element, save=save))

        elif element.get('type') == 'view':
            elements.append(import_view(element, save=save))

    return elements
