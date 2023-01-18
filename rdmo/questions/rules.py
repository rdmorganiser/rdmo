import logging
import rules

from rdmo.projects.rules import is_project_member, is_site_manager

logger = logging.getLogger(__name__)

@rules.predicate
def is_element_editor(user, obj) -> bool:
    ''' Checks if the user is an editor for the sites to which this element is available '''

    if not hasattr(obj, 'sites'):
        logger.debug('questions.rules.%s: obj %s has no attribute %s', is_element_editor, obj, 'sites')
        return False

    user_is_element_editor = user.role.editor.filter(id__in=obj.sites.all()).exists()
    return user_is_element_editor

@rules.predicate
def is_multisite_editor(user):
    ''' checks if the user is a multisite editor '''
    if not user.is_authenticated:
        return False
    if not hasattr(user.role, 'is_multisite_editor'):
        logger.debug('questions.rules.%s: obj %s has no attribute %s', 'is_multisite_editor', user.role, 'is_multisite_editor')
        return False
    return user.role.is_multisite_editor


@rules.predicate
def has_role_editor(user):
    ''' checks if the user is an editor at all'''
    return user.role.editor.exists()


@rules.predicate
def in_group_editors(user):
    ''' checks if the user is in group reviewer at all'''
    return user.groups.filter(name='editor').exists()


@rules.predicate
def in_group_reviewers(user):
    ''' checks if the user is in group reviewer at all'''
    return user.groups.filter(name='reviewer').exists()


rules.add_perm('questions.view_catalog_object', is_multisite_editor | has_role_editor | in_group_editors | in_group_reviewers)
rules.add_perm('questions.change_catalog_object', is_multisite_editor | is_element_editor)
rules.add_perm('questions.delete_catalog_object', is_multisite_editor | is_element_editor)


rules.add_perm('questions.view_section_object', is_multisite_editor | has_role_editor | in_group_editors | in_group_reviewers)
rules.add_perm('questions.change_section_object', is_multisite_editor | is_element_editor)
rules.add_perm('questions.delete_section_object', is_multisite_editor | is_element_editor)

# extra permissions for project members and site_managers
rules.add_perm('questions.view_questionset_object', (is_multisite_editor | has_role_editor | in_group_editors | in_group_reviewers) | (is_project_member | is_site_manager))
rules.add_perm('questions.change_questionset_object', is_multisite_editor | is_element_editor)
rules.add_perm('questions.delete_questionset_object', is_multisite_editor | is_element_editor)

rules.add_perm('questions.view_question_object', is_multisite_editor | has_role_editor | in_group_editors | in_group_reviewers)
rules.add_perm('questions.change_question_object', is_multisite_editor | is_element_editor)
rules.add_perm('questions.delete_question_object', is_multisite_editor | is_element_editor)
