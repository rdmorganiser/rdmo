import logging

from django.db import models
from django.contrib.sites.models import Site

import rules
from rules.predicates import is_superuser

logger = logging.getLogger(__name__)


@rules.predicate
def is_editor(user) -> bool:
    ''' Checks if any editor role exists for the user '''
    return user.role.editor.exists()


@rules.predicate
def is_multisite_editor(user) -> bool:
    ''' Checks if the user is an editor for all the sites '''
    if not is_editor(user):
        return False
    return user.role.editor.count() == Site.objects.count()


@rules.predicate
def is_element_editor(user, obj) -> bool:
    ''' Checks if the user is an editor for the sites to which this element is editable '''
    if obj is None:
        return user.role.editor.exists()

    if not obj.editors.exists():
        # if the element has no editors, it is editable by all users with an editor role
        return user.role.editor.exists()
    # else, return whether the user is an editor for the object
    return user.role.editor.filter(id__in=obj.editors.all()).exists()


@rules.predicate
def is_reviewer(user) -> bool:
    ''' Checks if any reviewer role exists for the user '''
    return user.role.reviewer.exists()


@rules.predicate
def is_multisite_reviewer(user) -> bool:
    ''' Checks if the user is an reviewer for all the sites '''
    if not user.role.reviewer.exists():
        return False
    return user.role.reviewer.count() == Site.objects.count()


@rules.predicate
def is_element_reviewer(user, obj) -> bool:
    ''' Checks if the user is an reviewer for the sites to which this element is editable '''
    if obj is None:
        return user.role.reviewer.exists()

    # if the element has no editors, it is reviewable by all reviewers
    if not obj.editors.exists():
        return user.role.reviewer.exists()

    # else, return whether the user is a reviewer for of the object
    return user.role.reviewer.filter(
        models.Q(id__in=obj.editors.all())
        ).exists()

# Add rules
rules.add_perm('can_view_management', is_editor | is_reviewer)


# Model Permissions for sites and group
rules.add_perm('sites.view_site', is_editor | is_reviewer)
rules.add_perm('auth.view_group', is_editor | is_reviewer)

# Model Permissions for domain
rules.add_perm('domain.view_attribute', is_editor | is_reviewer)
rules.add_perm('domain.add_attribute', is_editor)


# Object permissions domain attribute objects
rules.add_perm('domain.view_attribute_object', is_editor | is_element_reviewer)
rules.add_perm('domain.add_attribute_object', is_editor)
rules.add_perm('domain.change_attribute_object', is_element_editor)
rules.add_perm('domain.delete_attribute_object', is_element_editor)

# Model Permissions for options
rules.add_perm('options.view_option', is_editor | is_reviewer)
rules.add_perm('options.add_option', is_editor)

# Object Permissions for options option objects
rules.add_perm('options.view_option_object', is_editor | is_element_reviewer)
rules.add_perm('options.add_option_object', is_editor)
rules.add_perm('options.change_option_object', is_element_editor)
rules.add_perm('options.delete_option_object', is_element_editor)

# Model Permissions for optionsets
rules.add_perm('options.view_optionset', is_editor | is_reviewer)
rules.add_perm('options.add_optionset', is_editor)

# Object Permissions for options optionset objects
rules.add_perm('options.view_optionset_object', is_editor | is_element_reviewer)
rules.add_perm('options.add_optionset_object', is_editor)
rules.add_perm('options.change_optionset_object', is_element_editor)
rules.add_perm('options.delete_optionset_object', is_element_editor)

# Model Permissions for conditions
rules.add_perm('conditions.view_condition', is_editor | is_reviewer)
rules.add_perm('conditions.add_condition', is_editor)

# Object Permissions for conditions
rules.add_perm('conditions.view_condition_object', is_editor | is_element_reviewer)
rules.add_perm('conditions.add_condition_object', is_editor)
rules.add_perm('conditions.change_condition_object', is_element_editor)
rules.add_perm('conditions.delete_condition_object', is_element_editor)

# Model Permissions for tasks
rules.add_perm('tasks.view_task', is_editor | is_reviewer)
rules.add_perm('tasks.add_task', is_editor)

# Object Permissions for tasks
rules.add_perm('tasks.view_task_object', is_editor | is_element_reviewer)
rules.add_perm('tasks.add_task_object', is_editor)
rules.add_perm('tasks.change_task_object', is_element_editor)
rules.add_perm('tasks.delete_task_object', is_element_editor)

# Model Permissions for views
rules.add_perm('views.view_view', is_editor | is_reviewer)
rules.add_perm('views.add_view', is_editor)

# Object Permissions for views
rules.add_perm('views.view_view_object', is_editor | is_element_reviewer)
rules.add_perm('views.add_view_object', is_editor)
rules.add_perm('views.change_view_object', is_element_editor)
rules.add_perm('views.delete_view_object', is_element_editor)
