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

ROLE_RANKS = {
    ROLE_OWNER: 3,
    ROLE_MANAGER: 2,
    ROLE_AUTHOR: 1,
    ROLE_GUEST: 0
}
