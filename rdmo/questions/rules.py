import logging
import rules

from rdmo.projects.rules import is_project_member, is_site_manager

logger = logging.getLogger(__name__)

@rules.predicate
def can_read_element(user, obj) -> bool:
    ''' Checks if the user is an editor for the sites to which this element is readable '''
    
    if not hasattr(obj, 'sites'):
        logger.debug('questions.rules.%s: obj %s has no attribute %s', 'can_read_element', obj, 'sites')
        return False

    return user.role.editor.filter(id__in=obj.sites.all()).exists()

@rules.predicate
def can_edit_element(user, obj) -> bool:
    ''' Checks if the user is an editor for the sites to which this element is editable '''

    if not hasattr(obj, 'editors'):
        logger.debug('questions.rules.%s: obj %s has no attribute %s', 'can_edit_element', obj, 'editors')
        return False
    
    return user.role.editor.filter(id__in=obj.editors.all()).exists()

@rules.predicate
def is_multisite_editor(user) -> bool:
    ''' checks if the user is a multisite editor '''
    if not user.is_authenticated:
        return False
    if not hasattr(user.role, 'is_multisite_editor'):
        logger.debug('questions.rules.%s: obj %s has no attribute %s', 'is_multisite_editor', user.role, 'is_multisite_editor')
        return False
    return user.role.is_multisite_editor

@rules.predicate
def in_group_editors(user) -> bool:
    ''' checks if the user is in group reviewer at all'''
    return user.groups.filter(name='editor').exists()


@rules.predicate
def in_group_reviewers(user) -> bool:
    ''' checks if the user is in group reviewer at all'''
    return user.groups.filter(name='reviewer').exists()

# for catalogs
rules.add_perm('questions.view_catalog_object', is_multisite_editor | can_read_element | in_group_editors | in_group_reviewers)
rules.add_perm('questions.add_catalog_object', is_multisite_editor | can_edit_element)
rules.add_perm('questions.change_catalog_object', is_multisite_editor | can_edit_element)
rules.add_perm('questions.delete_catalog_object', is_multisite_editor | can_edit_element)

# for sections
rules.add_perm('questions.view_section_object', is_multisite_editor | can_read_element | in_group_editors | in_group_reviewers)
rules.add_perm('questions.add_section_object', is_multisite_editor | can_edit_element)
rules.add_perm('questions.change_section_object', is_multisite_editor | can_edit_element)
rules.add_perm('questions.delete_section_object', is_multisite_editor | can_edit_element)

# for questionsets and extra permissions imported from projects for project_member or site_manager
rules.add_perm('questions.view_questionset_object', (is_multisite_editor | can_read_element | in_group_editors | in_group_reviewers) | (is_project_member | is_site_manager))
rules.add_perm('questions.add_questionset_object', is_multisite_editor | can_edit_element)
rules.add_perm('questions.change_questionset_object', is_multisite_editor | can_edit_element)
rules.add_perm('questions.delete_questionset_object', is_multisite_editor | can_edit_element)

# for questions
rules.add_perm('questions.view_question_object', is_multisite_editor | can_read_element | in_group_editors | in_group_reviewers)
rules.add_perm('questions.add_question_object', is_multisite_editor | can_edit_element)
rules.add_perm('questions.change_question_object', is_multisite_editor | can_edit_element)
rules.add_perm('questions.delete_question_object', is_multisite_editor | can_edit_element)
