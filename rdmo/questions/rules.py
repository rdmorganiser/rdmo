
import rules

from rdmo.projects.rules import is_project_member, is_site_manager

@rules.predicate
def is_element_editor(user, obj) -> bool:
    ''' Checks if the user is an editor for the sites to which this element is available '''

    # # breakpoint()
    # if not user.is_authenticated:
    #     return False  # user is not authenticated

    # if not user.role.editor.exists():
    #     return False  # user is not an editor at all

    # if user.is_superuser:
    #     return True  # user is admin/superuser, staff or instance editor

    if not hasattr(obj, 'sites'):
        print('AttributeError sites for : ', obj)
        return False
    
    user_is_editor_for_obj = user.role.editor.filter(id__in=obj.sites.all()).exists()
    # print('\t\n !!! is_element_editor check: ', obj, user, user_is_editor_for_obj, '\n')
    # breakpoint()
    return user_is_editor_for_obj
    # return obj.can_edit_element(user)

@rules.predicate
def is_multisite_editor(user):
    ''' checks if the user is an instance editor '''
    if not user.is_authenticated:
        return False
    if not hasattr(user.role, 'is_multisite_editor'):
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

# from field sites
rules.add_perm('questions.view_catalog_object', has_role_editor | in_group_editors | in_group_reviewers | is_multisite_editor)
rules.add_perm('questions.change_catalog_object', is_element_editor | is_multisite_editor)
rules.add_perm('questions.delete_catalog_object', is_element_editor | is_multisite_editor)


rules.add_perm('questions.view_section_object', has_role_editor | in_group_editors | in_group_reviewers | is_multisite_editor)
rules.add_perm('questions.change_section_object', is_element_editor | is_multisite_editor)
rules.add_perm('questions.delete_section_object', is_element_editor | is_multisite_editor)

# extra permissions for project members and site_managers
rules.add_perm('questions.view_questionset_object', ( has_role_editor | in_group_editors | in_group_reviewers | is_multisite_editor) | ( is_project_member | is_site_manager ))
rules.add_perm('questions.change_questionset_object', is_element_editor | is_multisite_editor)
rules.add_perm('questions.delete_questionset_object', is_element_editor | is_multisite_editor)

rules.add_perm('questions.view_question_object', has_role_editor | in_group_editors | in_group_reviewers | is_multisite_editor)
rules.add_perm('questions.change_question_object', is_element_editor | is_multisite_editor)
rules.add_perm('questions.delete_question_object', is_element_editor | is_multisite_editor)
