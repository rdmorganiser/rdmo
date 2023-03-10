import logging

from django.db import models
from django.contrib.sites.models import Site

import rules

logger = logging.getLogger(__name__)


@rules.predicate
def is_an_editor(user) -> bool:
    ''' Checks if any editor role exists for the user '''
    return user.role.editor.exists()


@rules.predicate
def is_multisite_editor(user) -> bool:
    ''' Checks if the user is an editor for all the sites '''
    if not is_an_editor(user):
        logger.debug('rules.is_multisite_editor: user %s has no role editor', user)
        return False
    return user.role.editor.count() == Site.objects.count()


@rules.predicate
def is_element_editor(user, obj) -> bool:
    ''' Checks if the user is an editor for the sites to which this element is editable '''
    try:
        if not obj.editors.exists():
            # if the element has no editors, it is editable by all users with an editor role
            return user.role.editor.exists()
        return user.role.editor.filter(id__in=obj.editors.all()).exists()
    except AttributeError:
        logger.debug('rules.is_element_editor: obj %s has no attribute editors', obj)
        return False


@rules.predicate
def is_a_reviewer(user) -> bool:
    ''' Checks if any reviewer role exists for the user '''
    return user.role.reviewer.exists()


@rules.predicate
def is_multisite_reviewer(user) -> bool:
    ''' Checks if the user is an reviewer for all the sites '''
    if not user.role.reviewer.exists():
        logger.debug('rules.is_multisite_reviewer: obj %s has no role reviewer', user)
        return False
    return user.role.reviewer.count() == Site.objects.count()


@rules.predicate
def is_element_reviewer(user, obj) -> bool:
    ''' Checks if the user is an reviewer for the sites to which this element is editable '''

    try:  # block for obj.editors field
        # if the element has no editors, it is viewables by all reviewers
        if not obj.editors.exists():
            return user.role.reviewer.exists()
        
        try:  # block for obj.sites field
            # if the element has no sites, it is viewables by all reviewers
            if not obj.sites.exists():
                return user.role.reviewer.exists()
            
            return user.role.reviewer.filter(
                models.Q(id__in=obj.editors.all()) | models.Q(id__in=obj.sites.all())
                ).exists()
        except AttributeError:
            logger.debug('rules.is_element_reviewer: obj %s has no attribute sites', obj)
            return user.role.reviewer.filter(id__in=obj.editors.all()).exists()
    except AttributeError:
        logger.debug('rules.is_element_reviewer: obj %s has no attribute editors', obj)
        return False


# Model Permissions for sites and group
rules.add_perm('sites.view_site', is_an_editor | is_a_reviewer)
rules.add_perm('auth.view_group', is_an_editor | is_a_reviewer)

# Model Permissions for domain
rules.add_perm('domain.view_attribute', is_an_editor | is_a_reviewer)
rules.add_perm('domain.add_attribute', is_an_editor)
rules.add_perm('domain.change_attribute', is_an_editor)
rules.add_perm('domain.delete_attribute', is_an_editor)

# Object permissions domain attribute objects
rules.add_perm('domain.view_attribute_object', is_an_editor | is_element_reviewer | is_multisite_reviewer)
rules.add_perm('domain.add_attribute_object', is_element_editor | is_multisite_editor)
rules.add_perm('domain.change_attribute_object', is_element_editor | is_multisite_editor)
rules.add_perm('domain.delete_attribute_object', is_element_editor | is_multisite_editor)

# Model Permissions for options
rules.add_perm('options.view_option', is_an_editor | is_a_reviewer)
rules.add_perm('options.add_option', is_an_editor)
rules.add_perm('options.change_option', is_an_editor)
rules.add_perm('options.delete_option', is_an_editor)

# Object Permissions for options option objects
rules.add_perm('options.view_option_object', is_an_editor | is_element_reviewer | is_multisite_reviewer)
rules.add_perm('options.add_option_object', is_element_editor | is_multisite_editor)
rules.add_perm('options.change_option_object', is_element_editor | is_multisite_editor)
rules.add_perm('options.delete_option_object', is_element_editor | is_multisite_editor)


# Model Permissions for optionsets
rules.add_perm('options.view_optionset', is_an_editor | is_a_reviewer)
rules.add_perm('options.add_optionset', is_an_editor)
rules.add_perm('options.change_optionset', is_an_editor)
rules.add_perm('options.delete_optionset', is_an_editor)

# Object Permissions for options optionset objects
rules.add_perm('options.view_optionset_object', is_an_editor | is_element_reviewer | is_multisite_reviewer)
rules.add_perm('options.add_optionset_object', is_element_editor | is_multisite_editor)
rules.add_perm('options.change_optionset_object', is_element_editor | is_multisite_editor)
rules.add_perm('options.delete_optionset_object', is_element_editor | is_multisite_editor)

# Model Permissions for conditions
rules.add_perm('conditions.view_condition', is_an_editor | is_a_reviewer)
rules.add_perm('conditions.add_condition', is_an_editor)
rules.add_perm('conditions.change_condition', is_an_editor)
rules.add_perm('conditions.delete_condition', is_an_editor)

# Object Permissions for conditions
rules.add_perm('conditions.view_condition_object', is_an_editor | is_element_reviewer | is_multisite_reviewer)
rules.add_perm('conditions.add_condition_object', is_element_editor | is_multisite_editor)
rules.add_perm('conditions.change_condition_object', is_element_editor | is_multisite_editor)
rules.add_perm('conditions.delete_condition_object', is_element_editor | is_multisite_editor)


# Model Permissions for tasks
rules.add_perm('tasks.view_task', is_an_editor | is_a_reviewer)
rules.add_perm('tasks.add_task', is_an_editor)
rules.add_perm('tasks.change_task', is_an_editor)
rules.add_perm('tasks.delete_task', is_an_editor)

# Object Permissions for tasks
rules.add_perm('tasks.view_task_object', is_an_editor | is_element_reviewer | is_multisite_reviewer)
rules.add_perm('tasks.add_task_object', is_element_editor | is_multisite_editor)
rules.add_perm('tasks.change_task_object', is_element_editor | is_multisite_editor)
rules.add_perm('tasks.delete_task_object', is_element_editor | is_multisite_editor)

# Model Permissions for views
rules.add_perm('views.view_view', is_an_editor | is_a_reviewer)
rules.add_perm('views.add_view', is_an_editor)
rules.add_perm('views.change_view', is_an_editor)
rules.add_perm('views.delete_view', is_an_editor)

# Object Permissions for views
rules.add_perm('views.view_view_object', is_an_editor | is_element_reviewer | is_multisite_reviewer)
rules.add_perm('views.add_view_object', is_element_editor | is_multisite_editor)
rules.add_perm('views.change_view_object', is_element_editor | is_multisite_editor)
rules.add_perm('views.delete_view_object', is_element_editor | is_multisite_editor)
