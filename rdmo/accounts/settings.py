from django.conf import settings

auth_app, auth_model = settings.AUTH_USER_MODEL.lower().split('.')

user_view_permission = (
  auth_app,
  auth_model,
  'view_{}'.format(auth_model)
)

GROUPS = ()
