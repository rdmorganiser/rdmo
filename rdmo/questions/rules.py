import logging
import rules

from django.contrib.sites.models import Site
from rdmo.projects.rules import is_project_member, is_site_manager

logger = logging.getLogger(__name__)

@rules.predicate
def can_edit_element(user, obj) -> bool:
    ''' Checks if the user is an editor for the sites to which this element is editable '''

    if not hasattr(obj, 'editors'):
        logger.debug('questions.rules.%s: obj %s has no attribute %s', 'can_edit_element', obj, 'editors')
        return False
    
    # if the element is not editable by any site, it is editable by all
    if not obj.editors.exists():
        return user.role.editor.exists()
    
    return user.role.editor.filter(id__in=obj.editors.all()).exists()

@rules.predicate
def is_multisite_editor(user) -> bool:
    ''' checks if the user is a multisite editor '''
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.role.editor.count() == Site.objects.count()
 
@rules.predicate
def in_a_group_with_view_permissions(user, obj) -> bool:
    ''' checks if the user is in a group that can view elements'''
    return user.groups.exists()

  
# user.groups.filter(name='api').exists()
# user.groups.filter(name='reviewer').exists()
# user.groups.filter(name='editor').exists()

# for catalogs
rules.add_perm('questions.view_catalog_object', is_multisite_editor | can_edit_element | (in_a_group_with_view_permissions))
rules.add_perm('questions.add_catalog_object', is_multisite_editor | can_edit_element)
rules.add_perm('questions.change_catalog_object', is_multisite_editor | can_edit_element)
rules.add_perm('questions.delete_catalog_object', is_multisite_editor | can_edit_element)

# for sections
rules.add_perm('questions.view_section_object', is_multisite_editor | can_edit_element | (in_a_group_with_view_permissions))
rules.add_perm('questions.add_section_object', is_multisite_editor | can_edit_element)
rules.add_perm('questions.change_section_object', is_multisite_editor | can_edit_element)
rules.add_perm('questions.delete_section_object', is_multisite_editor | can_edit_element)

# for questionsets and extra permissions imported from projects for project_member or site_manager
rules.add_perm('questions.view_questionset_object', is_multisite_editor | can_edit_element | (in_a_group_with_view_permissions) | (is_project_member | is_site_manager))
rules.add_perm('questions.add_questionset_object', is_multisite_editor | can_edit_element)
rules.add_perm('questions.change_questionset_object', is_multisite_editor | can_edit_element)
rules.add_perm('questions.delete_questionset_object', is_multisite_editor | can_edit_element)

# for questions
rules.add_perm('questions.view_question_object', is_multisite_editor | can_edit_element | (in_a_group_with_view_permissions))
rules.add_perm('questions.add_question_object', is_multisite_editor | can_edit_element)
rules.add_perm('questions.change_question_object', is_multisite_editor | can_edit_element)
rules.add_perm('questions.delete_question_object', is_multisite_editor | can_edit_element)
