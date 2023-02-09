import logging

from django.contrib.sites.models import Site

import rules

logger = logging.getLogger(__name__)


@rules.predicate
def is_element_editor(user, obj) -> bool:
    ''' Checks if the user is an editor for the sites to which this element is editable '''
    if 'project' in obj._meta.model_name:
        return False

    if not hasattr(obj, 'editors'):
        logger.debug('questions.rules.is_element_editor: obj %s has no attribute editors', obj)
        return False

    # if the element has no editors, it is editable by all editors
    if not obj.editors.exists():
        return user.role.editor.exists()

    return user.role.editor.filter(id__in=obj.editors.all()).exists()

@rules.predicate
def is_multisite_editor(user, obj) -> bool:
    ''' Checks if the user is an editor for all the sites '''
    if not user.role.editor.exists():
        logger.debug('rules.is_multisite_editor: obj %s has no role editor', user)
        return False
    return user.role.editor.count() == Site.objects.count()

# Model permissions for questions app
# for catalogs
rules.add_perm('questions.view_catalog', is_multisite_editor)
rules.add_perm('questions.add_catalog', is_multisite_editor)
rules.add_perm('questions.change_catalog', is_multisite_editor)
rules.add_perm('questions.delete_catalog', is_multisite_editor)

# for sections
rules.add_perm('questions.view_section', is_multisite_editor)
rules.add_perm('questions.add_section', is_multisite_editor)
rules.add_perm('questions.change_section', is_multisite_editor)
rules.add_perm('questions.delete_section', is_multisite_editor)

# for questionsets
rules.add_perm('questions.add_questionset', is_multisite_editor)
rules.add_perm('questions.change_questionset', is_multisite_editor)
rules.add_perm('questions.delete_questionset', is_multisite_editor)

# for questions
rules.add_perm('questions.view_question', is_multisite_editor)
rules.add_perm('questions.add_question', is_multisite_editor)
rules.add_perm('questions.change_question', is_multisite_editor)
rules.add_perm('questions.delete_question', is_multisite_editor)


# Object permissions
# for catalogs
rules.add_perm('questions.view_catalog_object', is_element_editor)
rules.add_perm('questions.add_catalog_object', is_element_editor)
rules.add_perm('questions.change_catalog_object', is_element_editor)
rules.add_perm('questions.delete_catalog_object', is_element_editor)

# for sections
rules.add_perm('questions.view_section_object', is_element_editor)
rules.add_perm('questions.add_section_object', is_element_editor)
rules.add_perm('questions.change_section_object', is_element_editor)
rules.add_perm('questions.delete_section_object', is_element_editor)

# for questionsets
rules.add_perm('questions.add_questionset_object', is_element_editor)
rules.add_perm('questions.change_questionset_object', is_element_editor)
rules.add_perm('questions.delete_questionset_object', is_element_editor)

# for questions
rules.add_perm('questions.view_question_object', is_element_editor)
rules.add_perm('questions.add_question_object', is_element_editor)
rules.add_perm('questions.change_question_object', is_element_editor)
rules.add_perm('questions.delete_question_object', is_element_editor)
