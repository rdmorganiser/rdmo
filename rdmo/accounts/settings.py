from django.conf import settings

auth_app, auth_model = settings.AUTH_USER_MODEL.lower().split('.')

user_view_permission = (
  auth_app,
  auth_model,
  'view_{}'.format(auth_model)
)

GROUPS = ( 
          # TODO move api permissions to rules in apps
          # api is basically a user with all roles
          # has all Model Permissions
  ('api', (
      user_view_permission,
      ('domain', 'attribute', 'add_attribute'),
      ('domain', 'attribute', 'change_attribute'),
      ('domain', 'attribute', 'delete_attribute'),
      ('domain', 'attribute', 'view_attribute'),
      
      ('options', 'option', 'add_option'),
      ('options', 'option', 'change_option'),
      ('options', 'option', 'delete_option'),
      ('options', 'option', 'view_option'),
      ('options', 'optionset', 'add_optionset'),
      ('options', 'optionset', 'change_optionset'),
      ('options', 'optionset', 'delete_optionset'),
      ('options', 'optionset', 'view_optionset'),
      
      ('conditions', 'condition', 'add_condition'),
      ('conditions', 'condition', 'change_condition'),
      ('conditions', 'condition', 'delete_condition'),
      ('conditions', 'condition', 'view_condition'),
    
      
      ('tasks', 'task', 'add_task'),
      ('tasks', 'task', 'change_task'),
      ('tasks', 'task', 'delete_task'),
      ('tasks', 'task', 'view_task'),
      ('views', 'view', 'add_view'),
      ('views', 'view', 'change_view'),
      ('views', 'view', 'delete_view'),
      ('views', 'view', 'view_view'),
      
      ('projects', 'project', 'add_project'),
      ('projects', 'project', 'change_project'),
      ('projects', 'project', 'delete_project'),
      ('projects', 'project', 'view_project'),
      ('projects', 'snapshot', 'add_snapshot'),
      ('projects', 'snapshot', 'change_snapshot'),
      ('projects', 'snapshot', 'delete_snapshot'),
      ('projects', 'snapshot', 'view_snapshot'),
      ('projects', 'value', 'add_value'),
      ('projects', 'value', 'change_value'),
      ('projects', 'value', 'delete_value'),
      ('projects', 'value', 'view_value'),
      ('projects', 'membership', 'add_membership'),
      ('projects', 'membership', 'change_membership'),
      ('projects', 'membership', 'delete_membership'),
      ('projects', 'membership', 'view_membership'),
      ('projects', 'issue', 'add_issue'),
      ('projects', 'issue', 'change_issue'),
      ('projects', 'issue', 'delete_issue'),
      ('projects', 'issue', 'view_issue'),
      ('projects', 'integration', 'add_integration'),
      ('projects', 'integration', 'change_integration'),
      ('projects', 'integration', 'delete_integration'),
      ('projects', 'integration', 'view_integration'),
  )),
)
