import rules

from rdmo.questions.rules import is_an_editor, is_a_reviewer

# Model Permissions for sites and group
rules.add_perm('sites.view_site', is_an_editor | is_a_reviewer)
rules.add_perm('auth.view_group', is_an_editor | is_a_reviewer)

# Model Permissions for domain
rules.add_perm('domain.view_attribute', is_an_editor | is_a_reviewer)
rules.add_perm('domain.add_attribute', is_an_editor)
rules.add_perm('domain.change_attribute', is_an_editor)
rules.add_perm('domain.delete_attribute', is_an_editor)

# Model Permissions for options
rules.add_perm('options.view_option', is_an_editor | is_a_reviewer)
rules.add_perm('options.add_option', is_an_editor)
rules.add_perm('options.change_option', is_an_editor)
rules.add_perm('options.delete_option', is_an_editor)

# Model Permissions for optionsets
rules.add_perm('options.view_optionset', is_an_editor | is_a_reviewer)
rules.add_perm('options.add_optionset', is_an_editor)
rules.add_perm('options.change_optionset', is_an_editor)
rules.add_perm('options.delete_optionset', is_an_editor)

# Model Permissions for conditions
rules.add_perm('conditions.view_condition', is_an_editor | is_a_reviewer)
rules.add_perm('conditions.add_condition', is_an_editor)
rules.add_perm('conditions.change_condition', is_an_editor)
rules.add_perm('conditions.delete_condition', is_an_editor)

# Model Permissions for tasks
rules.add_perm('tasks.view_task', is_an_editor | is_a_reviewer)
rules.add_perm('tasks.add_task', is_an_editor)
rules.add_perm('tasks.change_task', is_an_editor)
rules.add_perm('tasks.delete_task', is_an_editor)

# Model Permissions for views
rules.add_perm('views.view_view', is_an_editor | is_a_reviewer)
rules.add_perm('views.add_view', is_an_editor)
rules.add_perm('views.change_view', is_an_editor)
rules.add_perm('views.delete_view', is_an_editor)
