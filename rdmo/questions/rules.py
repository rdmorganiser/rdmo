import logging

from django.db import models
from django.contrib.sites.models import Site

import rules

logger = logging.getLogger(__name__)

@rules.predicate
def is_an_editor(user, obj) -> bool:
    ''' Checks if any editor role exsits for the user '''
    if not user.is_authenticated:
        return False
    return user.role.editor.exists()

@rules.predicate
def is_a_reviewer(user, obj) -> bool:
    ''' Checks if any reviewer role exsits for the user '''
    if not user.is_authenticated:
        return False
    return user.role.reviewer.exists()


@rules.predicate
def is_element_editor(user, obj) -> bool:
    ''' Checks if the user is an editor for the sites to which this element is editable '''
    if not user.is_authenticated:
        return False

    if 'project' in obj._meta.model_name:
        return False

    if not hasattr(obj, 'editors'):
        logger.debug('rules.is_element_editor: obj %s has no attribute editors', obj)
        return False

    # if the element has no editors, it is editable by all editors
    if not obj.editors.exists():
        return user.role.editor.exists()


@rules.predicate
def is_element_reviewer(user, obj) -> bool:
    ''' Checks if the user is an reviewer for the sites to which this element is editable '''
    if not user.is_authenticated:
        return False

    if 'project' in obj._meta.model_name:
        return False

    if not hasattr(obj, 'editors'):
        logger.debug('rules.is_element_reviewer: obj %s has no attribute editors', obj)
        return False

    # if the element has no editors, it is viewables by all reviewers
    if not obj.editors.exists():
        return user.role.reviewer.exists()
    
    if hasattr(obj, 'sites'):
        obj_related_to_reviewer = user.role.reviewer.filter(
        models.Q(id__in=obj.editors.all()) | models.Q(id__in=obj.sites.all())
        ).exists()
    else:
        obj_related_to_reviewer = user.role.reviewer.filter(id__in=obj.editors.all()).exists()

    return obj_related_to_reviewer

@rules.predicate
def is_multisite_editor(user, obj) -> bool:
    ''' Checks if the user is an editor for all the sites '''
    if not user.is_authenticated:
        return False

    if not user.role.editor.exists():
        logger.debug('rules.is_multisite_editor: obj %s has no role editor', user)
        return False
    return user.role.editor.count() == Site.objects.count()


# Model permissions for questions app
# for catalogs
rules.add_perm('questions.view_catalog', is_an_editor | is_a_reviewer)
rules.add_perm('questions.add_catalog', is_an_editor)
rules.add_perm('questions.change_catalog', is_an_editor)
rules.add_perm('questions.delete_catalog', is_an_editor)

# for sections
rules.add_perm('questions.view_section', is_an_editor | is_a_reviewer)
rules.add_perm('questions.add_section', is_an_editor)
rules.add_perm('questions.change_section', is_an_editor)
rules.add_perm('questions.delete_section', is_an_editor)

# for questionsets
rules.add_perm('questions.view_questionset', is_an_editor | is_a_reviewer)
rules.add_perm('questions.add_questionset', is_an_editor)
rules.add_perm('questions.change_questionset', is_an_editor)
rules.add_perm('questions.delete_questionset', is_an_editor)

# for questions
rules.add_perm('questions.view_question', is_an_editor | is_a_reviewer)
rules.add_perm('questions.add_question', is_an_editor)
rules.add_perm('questions.change_question', is_an_editor)
rules.add_perm('questions.delete_question', is_an_editor)


# Object permissions
# for catalogs
rules.add_perm('questions.view_catalog_object', is_an_editor | is_element_reviewer)
rules.add_perm('questions.add_catalog_object', is_multisite_editor | is_element_editor)
rules.add_perm('questions.change_catalog_object', is_multisite_editor | is_element_editor)
rules.add_perm('questions.delete_catalog_object', is_multisite_editor | is_element_editor)

# for sections
rules.add_perm('questions.view_section_object', is_an_editor | is_element_reviewer)
rules.add_perm('questions.add_section_object', is_multisite_editor | is_element_editor)
rules.add_perm('questions.change_section_object', is_multisite_editor | is_element_editor)
rules.add_perm('questions.delete_section_object', is_multisite_editor | is_element_editor)

# for questionsets
rules.add_perm('questions.add_questionset_object', is_multisite_editor | is_element_editor)
rules.add_perm('questions.change_questionset_object', is_multisite_editor | is_element_editor)
rules.add_perm('questions.delete_questionset_object', is_multisite_editor | is_element_editor)

# for questions
rules.add_perm('questions.view_question_object', is_an_editor | is_element_reviewer)
rules.add_perm('questions.add_question_object', is_multisite_editor | is_element_editor)
rules.add_perm('questions.change_question_object', is_multisite_editor | is_element_editor)
rules.add_perm('questions.delete_question_object', is_multisite_editor | is_element_editor)
