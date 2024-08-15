from django.utils.translation import gettext_lazy as _

ROLE_OWNER = 'owner'
ROLE_MANAGER = 'manager'
ROLE_AUTHOR = 'author'
ROLE_GUEST = 'guest'
ROLE_CHOICES = (
    (ROLE_OWNER, _('Owner')),
    (ROLE_MANAGER, _('Manager')),
    (ROLE_AUTHOR, _('Author')),
    (ROLE_GUEST, _('Guest')),
)

VISIBILITY_PRIVATE = 'private'
VISIBILITY_INTERNAL = 'internal'
VISIBILITY_CHOICES = (
    (VISIBILITY_PRIVATE, _('Private')),
    (VISIBILITY_INTERNAL, _('Internal'))
)
